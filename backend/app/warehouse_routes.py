from flask import Blueprint, request, jsonify, session
from app.db import SessionLocal
from app.models.order import Order
from app.models.product import Product
import json

warehouse_routes = Blueprint('warehouse_routes', __name__)

@warehouse_routes.route('/api/warehouse/orders/<int:order_id>/fulfill', methods=['POST'])
def fulfill_order(order_id):
    if session.get('role') != 'warehouse':
        return jsonify({'error': 'Unauthorized'}), 401

    db = SessionLocal()
    try:
        order = db.query(Order).filter_by(id=order_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        if order.status != 'pending':
            return jsonify({'error': 'Order already fulfilled or invalid status'}), 400

        try:
            items = json.loads(order.items)
        except Exception:
            return jsonify({'error': 'Invalid order items format'}), 400

        for item in items:
            sku = item['sku']
            quantity = item['quantity']

            product = db.query(Product).filter_by(sku=sku).first()
            if not product:
                return jsonify({'error': f"Product with SKU {sku} not found"}), 404
            if product.stock_quantity < quantity:
                return jsonify({'error': f"Insufficient stock for SKU {sku}"}), 400

            product.stock_quantity -= quantity

        order.status = 'fulfilled'
        db.commit()
        return jsonify({'message': 'Order fulfilled and stock updated'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@warehouse_routes.route('/api/warehouse/orders/<int:order_id>/edit', methods=['POST'])
def edit_order(order_id):
    if 'user_id' not in session or session.get('role') != 'warehouse':
        return jsonify({"error": "Unauthorized"}), 401

    db = SessionLocal()
    try:
        order = db.query(Order).filter_by(id=order_id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        if order.status != 'pending':
            return jsonify({"error": "Only pending orders can be edited"}), 400

        data = request.get_json()
        updated_items = data.get('items')

        if not updated_items or not isinstance(updated_items, list):
            return jsonify({"error": "Invalid or missing items list"}), 400

        order.items = json.dumps(updated_items)
        db.commit()

        return jsonify({"message": "Order updated successfully"})
    except Exception as e:
        print("Edit error:", e)
        return jsonify({"error": "Something went wrong"}), 500
    finally:
        db.close()
