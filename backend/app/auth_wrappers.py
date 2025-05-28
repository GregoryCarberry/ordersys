from functools import wraps
from flask import session, jsonify

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Authentication required."}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_role = session.get('role')
            if user_role not in roles:
                return jsonify({"error": "You do not have access to this resource."}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

def require_permission(*required_perms):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            permissions = session.get('permissions', [])
            if not all(perm in permissions for perm in required_perms):
                return jsonify({"error": "You do not have the required permission(s)."}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
