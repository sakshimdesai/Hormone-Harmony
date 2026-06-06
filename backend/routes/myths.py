from flask import render_template
from db import get_db

def view_myths():
    db = get_db()

    myths = db.execute("""
        SELECT * FROM myths
    """).fetchall()

    return render_template(
        "myths.html",
        myths=myths
    )