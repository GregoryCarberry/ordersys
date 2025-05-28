from flask import session
from .db import get_user_from_db

def refresh_user_permissions(username):
    """
    Reloads the user's permissions and can_grant_permissions from the DB into session.
    """
    user = get_user_from_db(username)
    if user:
        session['permissions'] = user.get('permissions', [])
        session['can_grant_permissions'] = user.get('can_grant_permissions', False)
