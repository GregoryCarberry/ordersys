from app.seed_users import seed_users
from app.seed_products import seed_products
from app.seed_orders import seed_orders

def run_all_seeds():
    print("🔄 Seeding users...")
    seed_users()
    print("🔄 Seeding products...")
    seed_products()
    print("🔄 Seeding orders...")
    seed_orders()
    print("✅ All seeds completed.")

if __name__ == "__main__":
    run_all_seeds()
