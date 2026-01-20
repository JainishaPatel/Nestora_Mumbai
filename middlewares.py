from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login", next=request.full_path))
        return func(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin access required", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function