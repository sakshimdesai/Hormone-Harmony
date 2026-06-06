from flask import Flask, render_template, request
from models import create_users_table
from auth import signup_user, login_user
from flask import session, redirect
from utils import login_required
from models import (
    create_users_table,
    create_daily_logs_table,
    create_myths_table,
    create_awareness_table,
    create_meals_table,
    create_selfcare_table
)
from routes.symptoms import log_symptom, view_logs
from routes.checker import symptom_checker
from routes.education import get_phase_info
from db import get_db
from datetime import datetime, timedelta
from routes.patterns import my_patterns
from routes.myths import view_myths
from routes.awareness import view_awareness
from routes.meals import view_meals
from routes.selfcare import view_selfcare


app = Flask(__name__)
app.secret_key = "hormone-harmony-secret-key"

create_users_table()
create_daily_logs_table()
create_myths_table()
create_awareness_table()
create_meals_table()
create_selfcare_table()

@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("welcome.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return signup_user()
    return render_template("signup.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return login_user()
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/log-symptom", methods=["GET", "POST"])
@login_required
def symptom_logger():
    if request.method == "POST":
        return log_symptom()
    return render_template("symptom_logger.html")

@app.route("/my-logs")
@login_required
def my_logs():
    return view_logs()

@app.route("/symptom-checker", methods=["GET", "POST"])
@login_required
def check_symptom():
    return symptom_checker()

@app.route("/cycle-wheel")
@login_required
def cycle_wheel():
    return render_template("cycle_wheel.html")

@app.route("/cycle-info/<phase>")
@login_required
def cycle_info(phase):
    return get_phase_info(phase)

@app.route('/my-patterns')
@login_required
def patterns_page():
    return my_patterns()

@app.route('/myths')
@login_required
def myths_page():
    return view_myths()

@app.route('/awareness')
@login_required
def awareness_page():
    return view_awareness()

@app.route('/meal-guide')
@login_required
def meal_guide():
    return view_meals()

@app.route('/selfcare')
@login_required
def selfcare_page():
    return view_selfcare()

if __name__ == "__main__":
    app.run(debug=True)
