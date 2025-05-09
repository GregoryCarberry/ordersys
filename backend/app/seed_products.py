from app.db import SessionLocal
from app.models.product import Product

# ✅ Sample product list
sample_products = [
    {"sku": "SHMP-001", "name": "Moisture Repair Shampoo", "barcode": "123456789012", "stock_quantity": 120, "low_stock_threshold": 10},
    {"sku": "CNDT-002", "name": "Smoothing Conditioner", "barcode": "123456789013", "stock_quantity": 85, "low_stock_threshold": 10},
    {"sku": "OIL-003", "name": "Argan Hair Oil", "barcode": "123456789014", "stock_quantity": 45, "low_stock_threshold": 10},
    {"sku": "SPR-004", "name": "Leave-In Detangler Spray", "barcode": "123456789015", "stock_quantity": 60, "low_stock_threshold": 10},
    {"sku": "MASK-005", "name": "Deep Repair Hair Mask", "barcode": "123456789016", "stock_quantity": 30, "low_stock_threshold": 10},
    {"sku": "SHMP-006", "name": "Volumizing Shampoo", "barcode": "123456789017", "stock_quantity": 75, "low_stock_threshold": 10},
    {"sku": "CNDT-007", "name": "Color Protect Conditioner", "barcode": "123456789018", "stock_quantity": 90, "low_stock_threshold": 10},
    {"sku": "TREAT-008", "name": "Keratin Treatment", "barcode": "123456789019", "stock_quantity": 40, "low_stock_threshold": 10},
    {"sku": "GEL-009", "name": "Styling Gel Strong Hold", "barcode": "123456789020", "stock_quantity": 70, "low_stock_threshold": 10},
    {"sku": "MOUSSE-010", "name": "Volumizing Mousse", "barcode": "123456789021", "stock_quantity": 50, "low_stock_threshold": 10},
    {"sku": "HAIRSPRAY-011", "name": "Flexible Hold Hairspray", "barcode": "123456789022", "stock_quantity": 60, "low_stock_threshold": 10},
    {"sku": "DRY-012", "name": "Dry Shampoo", "barcode": "123456789023", "stock_quantity": 45, "low_stock_threshold": 10},
    {"sku": "OIL-013", "name": "Coconut Hair Oil", "barcode": "123456789024", "stock_quantity": 35, "low_stock_threshold": 10},
    {"sku": "SHMP-014", "name": "Anti-Dandruff Shampoo", "barcode": "123456789025", "stock_quantity": 80, "low_stock_threshold": 10},
    {"sku": "CNDT-015", "name": "Hydrating Conditioner", "barcode": "123456789026", "stock_quantity": 65, "low_stock_threshold": 10},
    {"sku": "MASK-016", "name": "Charcoal Detox Hair Mask", "barcode": "123456789027", "stock_quantity": 25, "low_stock_threshold": 10},
    {"sku": "COMB-017", "name": "Wide-Tooth Comb", "barcode": "123456789028", "stock_quantity": 100, "low_stock_threshold": 10},
    {"sku": "BRUSH-018", "name": "Round Brush Large", "barcode": "123456789029", "stock_quantity": 85, "low_stock_threshold": 10},
    {"sku": "CLIP-019", "name": "Sectioning Hair Clips (Set of 4)", "barcode": "123456789030", "stock_quantity": 200, "low_stock_threshold": 10},
    {"sku": "TREAT-020", "name": "Split End Repair Serum", "barcode": "123456789031", "stock_quantity": 40, "low_stock_threshold": 10},
    {"sku": "OIL-021", "name": "Jojoba Nourishing Oil", "barcode": "123456789032", "stock_quantity": 55, "low_stock_threshold": 10},
    {"sku": "SPR-022", "name": "Curl Enhancing Spray", "barcode": "123456789033", "stock_quantity": 35, "low_stock_threshold": 10},
    {"sku": "GEL-023", "name": "Medium Hold Styling Gel", "barcode": "123456789034", "stock_quantity": 60, "low_stock_threshold": 10},
    {"sku": "SHMP-024", "name": "Clarifying Shampoo", "barcode": "123456789035", "stock_quantity": 45, "low_stock_threshold": 10},
    {"sku": "CNDT-025", "name": "Reconstruction Conditioner", "barcode": "123456789036", "stock_quantity": 70, "low_stock_threshold": 10},
    {"sku": "CAPE-026", "name": "Salon Cutting Cape", "barcode": "123456789037", "stock_quantity": 20, "low_stock_threshold": 10},
    {"sku": "GLOVE-027", "name": "Latex-Free Gloves (Box of 100)", "barcode": "123456789038", "stock_quantity": 15, "low_stock_threshold": 10},
    {"sku": "NECKSTRIP-028", "name": "Neck Strips Roll", "barcode": "123456789039", "stock_quantity": 90, "low_stock_threshold": 10},
    {"sku": "TOWEL-029", "name": "Microfiber Hair Towels", "barcode": "123456789040", "stock_quantity": 50, "low_stock_threshold": 10},
    {"sku": "COLOR-030", "name": "Hair Colour Kit - Warm Brown", "barcode": "123456789041", "stock_quantity": 30, "low_stock_threshold": 10}
]



def seed_products():
    db = SessionLocal()
    created = 0
    try:
        for data in sample_products:
            if not db.query(Product).filter_by(sku=data["sku"]).first():
                db.add(Product(**data))
                created += 1
        db.commit()
        print(f"[✔] Seeded {created} new products.")
    except Exception as e:
        print(f"[!] Error seeding products: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
