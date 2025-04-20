# backend/app/permissions.py

from functools import wraps
from flask import session, redirect, url_for
from datetime import datetime

# Define default permissions for each role
ROLE_DEFAULTS = {
    'root': ['*'],  # All permissions
    'warehouse_manager': ['view_stock', 'edit_stock', 'approve_orders', 'grant_permissions'],
    'store_manager': ['view_products', 'make_orders'],
    'store_staff': ['view_products'],
    'owner': ['view_reports'],
}

def has_permission(required_permission):
    permissions = session.get('permissions', [])
    if '*' in permissions:
        return True
    return required_permission in permissions

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not has_permission(permission):
                return redirect(url_for('unauthorized'))  # you should define this route
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def refresh_user_permissions(user):
    """
    Returns a list of active permissions for a user, combining stored permissions
    with role defaults, and filtering out any that are expired.
    """
    permissions = user.get('permissions', [])

    if '*' in permissions:
        return ['*']  # Superuser

    now = datetime.now()
    active_permissions = []

    for perm in permissions:
        if isinstance(perm, dict):
            expires = perm.get('expires_at')
            if not expires or datetime.strptime(expires, '%Y-%m-%d %H:%M:%S') > now:
                active_permissions.append(perm['permission'])
        else:
            active_permissions.append(perm)

    # Add default role permissions if not already present
    defaults = ROLE_DEFAULTS.get(user['role'], [])
    for p in defaults:
        if p not in active_permissions:
            active_permissions.append(p)

    return active_permissions
