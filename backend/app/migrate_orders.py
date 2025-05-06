import json
from app.db import SessionLocal
from app.models.order import Order

def parse_legacy_format(items_text):
    """
    Converts a simple string format like:
    'SHMP-001 x 2, OIL-003 x 1'
    into:
    [{"sku": "SHMP-001", "quantity": 2}, {"sku": "OIL-003", "quantity": 1}]
    """
    result = []
    try:
        parts = items_text.split(',')
        for part in parts:
            part = part.strip()
            if 'x' in part:
                sku, qty = part.split('x')
                result.append({"sku": sku.strip(), "quantity": int(qty.strip())})
    except Exception as e:
        print(f"[!] Failed to parse legacy format: {items_text}")
        return None
    return result

def migrate_orders():
    db = SessionLocal()
    updated = 0

    try:
        orders = db.query(Order).all()
        for order in orders:
            try:
                # If it's already JSON, this will work
                parsed = json.loads(order.items)
                if isinstance(parsed, list):
                    continue  # Already in correct format
            except Exception:
                # Not JSON — likely legacy text format
                fixed = parse_legacy_format(order.items)
                if fixed:
                    order.items = json.dumps(fixed)
                    updated += 1

        db.commit()
        print(f"[✔] Migration complete. Updated {updated} order(s).")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_orders()
