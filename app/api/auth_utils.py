from functools import wraps
from flask import abort
from app.api.auth import token_auth

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = token_auth.current_user()
        if not current_user or not current_user.is_admin:
            abort(403, description="Admin privileges required")
        return f(*args, **kwargs)
    return decorated_function