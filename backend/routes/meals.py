from flask import render_template
from db import get_db

def view_meals():
    db = get_db()

    meals = db.execute("""
        SELECT * FROM meals
    """).fetchall()

    return render_template(
        "meals.html",
        meals=meals
    )