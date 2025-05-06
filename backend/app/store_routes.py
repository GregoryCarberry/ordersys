from flask import Blueprint, jsonify, session, request
from app.db import SessionLocal
from app.models.order import Order
import json
from app.models.product import Product  # add this if not already
from sqlalchemy import or_

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

@store_routes.route('/api/store/orders', methods=['POST'])
def create_order():
    if 'user_id' not in session or 'store_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or 'items' not in data:
        return jsonify({'error': 'Missing items in request'}), 400

    try:
        items_json = json.dumps(data['items'])  # Store items as JSON string
        new_order = Order(
            store_id=session['store_id'],
            items=items_json,
            status='pending'
        )

        db = SessionLocal()
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        db.close()

        return jsonify({
            'message': 'Order created successfully',
            'order_id': new_order.id
        }), 201

    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@store_routes.route('/api/products/search')
def search_products():
    if 'user_id' not in session or 'store_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])

    db = SessionLocal()
    try:
        products = db.query(Product).filter(
            Product.active == True,
            or_(
                Product.name.ilike(f"%{query}%"),
                Product.sku.ilike(f"%{query}%"),
                Product.barcode.ilike(f"%{query}%")
            )
        ).limit(10).all()

        result = []
        for p in products:
            result.append({
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "barcode": p.barcode
            })

        return jsonify(result)
    finally:
        db.close()