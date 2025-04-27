from flask import Blueprint, render_template, redirect, url_for, session, abort, request, jsonify
from functools import wraps
from app.db import db
from app.models.store import Store

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Session contents:", dict(session))  # <<<<<< DEBUG
        if session.get('role') not in ['admin', 'root']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function



@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    print("SESSION DEBUG at dashboard:", dict(session))  # <<<<<< DEBUG
    # Dummy stats for now
    stats = {
        'total_users': 23,
        'total_stores': 6,
        'orders_this_week': 45
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@admin_required
def manage_users():
    return render_template('admin/manage_users.html')

@admin_bp.route('/stores')
@admin_required
def manage_stores():
    return render_template('admin/manage_stores.html')

@admin_bp.route('/orders')
@admin_required
def manage_orders():
    return render_template('admin/manage_orders.html')

@admin_bp.route('/api/users')
@admin_required
def get_users_api():
    # Dummy data for now until you hook real DB
    users = [
        {"id": 1, "username": "admin", "role": "warehouse_manager", "store_id": None, "active": True},
        {"id": 2, "username": "storemanager1", "role": "store_manager", "store_id": 1, "active": True},
        {"id": 3, "username": "staff1", "role": "store_staff", "store_id": 1, "active": True},
    ]
    return users  # Flask automatically jsonify()'s lists/dicts

@admin_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user_api(user_id):
    print(f"Deleting user {user_id}")  # You can remove later
    # TODO: Delete from database
    return jsonify({"message": f"User {user_id} deleted"}), 200

@admin_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def edit_user_api(user_id):
    data = request.get_json()
    print(f"Updating user {user_id} with data: {data}")
    # TODO: Update the database here
    return jsonify({"message": f"User {user_id} updated"}), 200

# Dummy store list to simulate a database
dummy_stores = [
    {"id": 1, "name": "Telford Central", "location": "Albion Street", "active": True},
    {"id": 2, "name": "Wellington", "location": "Station Road", "active": True},
    {"id": 3, "name": "Oakengates", "location": "", "active": False}
]

@admin_bp.route('/api/stores', methods=['GET'])
@admin_required
def get_stores():
    stores = Store.query.all()
    return jsonify([
        {
            'id': store.id,
            'name': store.name,
            'location': store.location,
            'active': store.active
        } for store in stores
    ])


@admin_bp.route('/api/stores', methods=['POST'])
@admin_required
def create_store():
    data = request.get_json()
    store = Store(
        name=data['name'],
        location=data.get('location', ''),
        active=data.get('active', True)
    )
    db.session.add(store)
    db.session.commit()
    return jsonify({"message": "Store created", "store_id": store.id}), 201


@admin_bp.route('/api/stores/<int:store_id>', methods=['PUT'])
@admin_required
def update_store(store_id):
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    store.name = data['name']
    store.location = data.get('location', '')
    store.active = data.get('active', True)
    db.session.commit()
    return jsonify({"message": "Store updated"})


@admin_bp.route('/api/stores/<int:store_id>', methods=['DELETE'])
@admin_required
def delete_store(store_id):
    store = Store.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return jsonify({"message": "Store deleted"})
