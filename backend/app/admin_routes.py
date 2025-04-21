from flask import Blueprint, render_template, redirect, url_for, session
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from flask import abort

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
