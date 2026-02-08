from flask import request, redirect
from db import get_db
from utils import login_required
from flask import session
from flask import render_template
from flask import flash


@login_required
def log_symptom():
    if request.method == "POST":
        date = request.form.get("date")
        period = request.form.get("period")
        mood = request.form.get("mood")
        energy = request.form.get("energy")
        cravings = request.form.get("cravings")
        symptoms = request.form.getlist("symptoms")

        cravings = 1 if cravings else 0
        symptoms_text = ",".join(symptoms)

        db = get_db()
        db.execute("""
            INSERT INTO daily_logs 
            (user_id, date, period, mood, energy, cravings, symptoms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            date,
            period,
            mood,
            energy,
            cravings,
            symptoms_text
        ))
        db.commit()
        flash("Your log was saved 💗", "success")

        return redirect("/dashboard")

    return redirect("/log-symptom")

@login_required
def view_logs():
    db = get_db()
    logs = db.execute(
        """
        SELECT date, period, mood, energy, cravings, symptoms
        FROM daily_logs
        WHERE user_id = ?
        ORDER BY date DESC
        """,
        (session["user_id"],)
    ).fetchall()

    return render_template("my_logs.html", logs=logs)
