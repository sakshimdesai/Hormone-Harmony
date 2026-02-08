from flask import request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

def signup_user():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return "Invalid details"

    db = get_db()

    # Check if user already exists
    existing_user = db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    # If user exists → auto login
    if existing_user:
        if check_password_hash(existing_user["password_hash"], password):
            session["user_id"] = existing_user["id"]
            return redirect("/dashboard")
        else:
            return "Account exists. Incorrect password."

    # New user signup
    if not name or len(password) < 8:
        return "Invalid details"

    password_hash = generate_password_hash(password)

    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )
    db.commit()

    # Auto login after signup
    user_id = db.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()["id"]

    session["user_id"] = user_id
    return redirect("/dashboard")


def login_user():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return "Invalid details"

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if user and check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]
        return redirect("/dashboard")

    return "Invalid email or password"
