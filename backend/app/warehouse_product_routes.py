from flask import Blueprint, jsonify, request, session
from app.db import SessionLocal
from app.models.product import Product

warehouse_products = Blueprint('warehouse_products', __name__)

# Middleware-style check
def is_warehouse_user():
    return session.get("role") == "warehouse"

@warehouse_products.route('/api/warehouse/products', methods=['GET'])
def get_products():
    if not is_warehouse_user():
        return jsonify({"error": "Unauthorized"}), 401

    db = SessionLocal()
    try:
        products = db.query(Product).all()
        return jsonify([
            {
                "sku": p.sku,
                "name": p.name,
                "barcode": p.barcode,
                "stock_quantity": p.stock_quantity
            } for p in products
        ])
    finally:
        db.close()

@warehouse_products.route('/api/warehouse/products', methods=['POST'])
def create_product():
    if not is_warehouse_user():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    db = SessionLocal()
    try:
        existing = db.query(Product).filter_by(sku=data['sku']).first()
        if existing:
            return jsonify({"error": "SKU already exists"}), 400

        new_product = Product(
            sku=data['sku'],
            name=data['name'],
            barcode=data.get('barcode', ''),
            stock_quantity=data.get('stock_quantity', 0)
        )
        db.add(new_product)
        db.commit()
        return jsonify({"message": "Product created"})
    finally:
        db.close()

@warehouse_products.route('/api/warehouse/products/<sku>', methods=['PUT'])
def update_product(sku):
    if not is_warehouse_user():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    db = SessionLocal()
    try:
        product = db.query(Product).filter_by(sku=sku).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404

        product.name = data.get('name', product.name)
        product.barcode = data.get('barcode', product.barcode)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        db.commit()
        return jsonify({"message": "Product updated"})
    finally:
        db.close()

@warehouse_products.route('/api/warehouse/products/<sku>', methods=['DELETE'])
def delete_product(sku):
    if not is_warehouse_user():
        return jsonify({"error": "Unauthorized"}), 401

    db = SessionLocal()
    try:
        product = db.query(Product).filter_by(sku=sku).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        db.delete(product)
        db.commit()
        return jsonify({"message": "Product deleted"})
    finally:
        db.close()
