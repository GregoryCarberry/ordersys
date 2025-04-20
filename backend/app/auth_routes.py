from flask import Blueprint, request, session, jsonify

auth_bp = Blueprint('auth', __name__)

# Hardcoded users
users = {
    "manager": "password123",
    "staff": "password123"
}

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Invalid content type"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        session['username'] = username
        session['role'] = "manager" if username == "manager" else "staff"
        session.permanent = True
        return jsonify({"logged_in": True, "username": username, "role": session['role']}), 200
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