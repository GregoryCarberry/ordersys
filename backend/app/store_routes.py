from flask import Blueprint, jsonify, session
from app.db import SessionLocal
from app.models.order import Order

store_routes = Blueprint('store_routes', __name__)



@store_routes.route('/api/store/orders', methods=['GET'])
def get_store_orders():

    # TEMPORARY FOR POSTMAN TESTING
    session['user_id'] = 1
    session['store_id'] = 1

    if 'user_id' not in session or 'store_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    store_id = session['store_id']

    db = SessionLocal()
    try:
        orders = db.query(Order).filter_by(store_id=store_id).order_by(Order.created_at.desc()).all()
        result = []
        for order in orders:
            result.append({
                'id': order.id,
                'items': order.items,
                'status': order.status,
                'created_at': order.created_at.isoformat()
            })
        return jsonify(result)
    finally:
        db.close()

@store_routes.route('/api/store/orders/<int:order_id>', methods=['GET'])
def get_order_detail(order_id):
    if 'user_id' not in session or 'store_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    db = SessionLocal()
    try:
        order = db.query(Order).filter_by(id=order_id, store_id=session['store_id']).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        return jsonify({
            'id': order.id,
            'items': order.items,
            'status': order.status,
            'created_at': order.created_at.isoformat()
        })
    finally:
        db.close()
