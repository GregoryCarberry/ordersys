from flask import Blueprint, jsonify
from app.db import SessionLocal
from app.models.order import Order
from app.models.product import Product
import json

order_admin_routes = Blueprint('order_admin_routes', __name__)

@order_admin_routes.route('/api/admin/orders/<int:order_id>/fulfill', methods=['PATCH'])
def fulfill_order(order_id):
    db = SessionLocal()
    try:
        order = db.query(Order).filter_by(id=order_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        if order.status != 'pending':
            return jsonify({'error': 'Order is not in pending state'}), 400

        try:
            items = json.loads(order.items)
        except Exception:
            return jsonify({'error': 'Invalid order item format'}), 400

        # Validate and deduct stock
        for item in items:
            sku = item.get('sku')
            qty = item.get('quantity', 0)

            product = db.query(Product).filter_by(sku=sku).first()
            if not product:
                return jsonify({'error': f'Product with SKU {sku} not found'}), 404

            if product.stock_quantity < qty:
                return jsonify({'error': f'Insufficient stock for SKU {sku}'}), 400

        # All good — deduct stock and fulfill order
        for item in items:
            product = db.query(Product).filter_by(sku=item['sku']).first()
            product.stock_quantity -= item['quantity']

        order.status = 'fulfilled'
        db.commit()

        return jsonify({'message': 'Order fulfilled successfully'}), 200

    finally:
        db.close()
