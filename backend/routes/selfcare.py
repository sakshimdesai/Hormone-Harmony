from flask import render_template
from db import get_db

def view_selfcare():
    db = get_db()

    entries = db.execute("""
        SELECT * FROM selfcare
    """).fetchall()

    return render_template(
        "selfcare.html",
        entries=entries
    )