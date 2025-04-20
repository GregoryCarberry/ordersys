# backend/app/auth_routes.py

from flask import Blueprint, request, session, jsonify
from werkzeug.security import check_password_hash
from app.db import get_user_from_db
from app.permissions import refresh_user_permissions

auth_bp = Blueprint('auth', __name__)

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

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

