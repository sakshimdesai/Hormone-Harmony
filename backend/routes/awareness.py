from flask import render_template
from db import get_db

def view_awareness():
    db = get_db()

    awareness_items = db.execute("""
        SELECT * FROM awareness
    """).fetchall()

    return render_template(
        "awareness.html",
        awareness_items=awareness_items
    )