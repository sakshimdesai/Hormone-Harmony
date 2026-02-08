from flask import session, redirect, flash
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this feature 🌸", "warning")
            return redirect("/login")
        return view_func(*args, **kwargs)
    return wrapper
