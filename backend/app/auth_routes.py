from flask import Blueprint, request, session, jsonify, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_user_from_db, get_db_connection, save_permissions_to_db
from app.permissions import refresh_user_permissions

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login_get():
    return redirect("http://localhost:3000/")  

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Invalid content type"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user_from_db(username)

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['store_id'] = user['store_id']
        session['can_grant_permissions'] = bool(user['can_grant_permissions'])
        session['permissions'] = refresh_user_permissions(user)
        session.permanent = True

        return jsonify({
            "logged_in": True,
            "username": user['username'],
            "role": user['role']
        }), 200

    return jsonify({"logged_in": False, "message": "Invalid credentials"}), 401

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'username' in session:
        return jsonify({
            "logged_in": True,
            "username": session.get('username'),
            "role": session.get('role')
        }), 200
    return jsonify({"logged_in": False}), 401

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login')) # Redirect to login page


@auth_bp.route('/grant-permissions', methods=['POST'])
def grant_permissions():
    if 'username' not in session:
        return jsonify({"error": "Not authenticated."}), 401

    current_username = session['username']
    current_user = get_user_from_db(current_username)

    if not current_user or not current_user.get('can_grant_permissions'):
        return jsonify({"error": "You are not authorized to grant permissions."}), 403

    data = request.get_json()
    target_username = data.get('target_username')
    new_permissions = data.get('permissions')

    if not target_username or not isinstance(new_permissions, list):
        return jsonify({"error": "Invalid request format."}), 400

    target_user = get_user_from_db(target_username)
    if not target_user:
        return jsonify({"error": "Target user not found."}), 404

    # Merge existing permissions with new ones (no duplicates)
    updated_permissions = list(set(target_user.get('permissions', []) + new_permissions))

    # Save back to database
    save_permissions_to_db(target_username, updated_permissions)

    return jsonify({"message": f"Permissions granted to {target_username} successfully."}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    if 'username' not in session:
        return jsonify({"error": "Not authenticated."}), 401

    current_username = session['username']
    current_user = get_user_from_db(current_username)

    if not current_user or not current_user.get('can_grant_permissions'):
        return jsonify({"error": "You are not authorized to create users."}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    store_id = data.get('store_id', 0)  # Default to 0 if not provided

    if not username or not password or not role:
        return jsonify({"error": "Username, password, and role are required."}), 400

    if get_user_from_db(username):
        return jsonify({"error": "User already exists."}), 400

    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password_hash, role, permissions, can_grant_permissions, store_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        username,
        password_hash,
        role,
        '[]',  # empty permissions initially
        0,     # cannot grant permissions unless elevated later
        store_id
    ))
    conn.commit()
    conn.close()

    return jsonify({"message": f"User '{username}' registered successfully."}), 201

@auth_bp.route('/get-permissions', methods=['POST'])
def get_permissions():
    if 'username' not in session:
        return jsonify({"error": "Not authenticated."}), 401

    data = request.get_json()
    target_username = data.get('target_username')

    if not target_username:
        return jsonify({"error": "Missing target_username field."}), 400

    target_user = get_user_from_db(target_username)

    if not target_user:
        return jsonify({"error": "Target user not found."}), 404

    return jsonify({
        "username": target_username,
        "permissions": target_user.get('permissions', [])
    }), 200

@auth_bp.route('/revoke-permissions', methods=['POST'])
def revoke_permissions():
    if 'username' not in session:
        return jsonify({"error": "Not authenticated."}), 401

    current_username = session['username']
    current_user = get_user_from_db(current_username)

    if not current_user or not current_user.get('can_grant_permissions'):
        return jsonify({"error": "You are not authorized to revoke permissions."}), 403

    data = request.get_json()
    target_username = data.get('target_username')
    permissions_to_revoke = data.get('permissions', [])

    if not target_username or not isinstance(permissions_to_revoke, list):
        return jsonify({"error": "Invalid request data."}), 400

    target_user = get_user_from_db(target_username)
    if not target_user:
        return jsonify({"error": "Target user not found."}), 404

    updated_permissions = [p for p in target_user['permissions'] if p not in permissions_to_revoke]
    save_permissions_to_db(target_username, updated_permissions)

    return jsonify({
        "message": f"Permissions revoked for {target_username}.",
        "current_permissions": updated_permissions
    }), 200
