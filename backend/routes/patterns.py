from flask import request, render_template, session
from datetime import datetime, timedelta
from utils import login_required
from db import get_db
from collections import Counter

@login_required
def my_patterns():
    user_id = session.get("user_id")
    db = get_db()

    # Time range filter
    days = request.args.get("days", "30")
    if days == "all":
        cutoff_date = "2000-01-01"
    else:
        cutoff_date = (datetime.now() - timedelta(days=int(days))).strftime("%Y-%m-%d")

    # ✅ MATCHES DB SCHEMA EXACTLY
    logs = db.execute("""
        SELECT date, period, mood, energy, cravings, symptoms
        FROM daily_logs
        WHERE user_id = ? AND date >= ?
        ORDER BY date ASC
    """, (user_id, cutoff_date)).fetchall()

    dates = []
    period_status = []
    mood_values = []
    energy_values = []
    symptom_counter = Counter()

    for log in logs:
        dates.append(log["date"])
        period_status.append(1 if log["period"] == 1 else 0)
        mood_values.append(log["mood"] or 0)
        energy_values.append(log["energy"] or 0)

        if log["symptoms"]:
            for s in log["symptoms"].split(","):
                s = s.strip()
                if s:
                    symptom_counter[s] += 1

    total_logs = len(logs)

    # Last period date
    last_period_date = None
    days_since_period = None
    for log in reversed(logs):
        if log["period"] == 1:
            last_period_date = log["date"]
            d = datetime.strptime(log["date"], "%Y-%m-%d")
            days_since_period = (datetime.now() - d).days
            break

    # Average mood emoji
    valid_moods = [m for m in mood_values if m > 0]
    mood_emojis = {1:"😢", 2:"😕", 3:"😐", 4:"🙂", 5:"😊"}
    if valid_moods:
        avg_mood = sum(valid_moods) / len(valid_moods)
        avg_mood_emoji = mood_emojis.get(round(avg_mood), "😐")
    else:
        avg_mood_emoji = "😐"

    # Symptom chart data
    top_symptoms = symptom_counter.most_common(6)

    chart_data = {
        "dates": dates,
        "period_status": period_status,
        "mood": mood_values,
        "energy": energy_values,
        "symptoms": {
            "labels": [s[0] for s in top_symptoms],
            "counts": [s[1] for s in top_symptoms]
        }
    }

    insights = generate_insights(logs, period_status, mood_values, energy_values, symptom_counter)

    return render_template(
        "my_patterns.html",
        total_logs=total_logs,
        last_period_date=last_period_date,
        days_since_period=days_since_period,
        avg_mood_emoji=avg_mood_emoji,
        chart_data=chart_data,
        insights=insights,
        selected_days=days
    )


def generate_insights(logs, period_status, mood_values, energy_values, symptom_counter):
    insights = []

    if len(logs) < 3:
        return ["Log a few more days to see personalized insights 🌸"]

    # Cycle regularity (based on period logs)
    period_days = [i for i, v in enumerate(period_status) if v == 1]
    if len(period_days) >= 2:
        gaps = [period_days[i+1] - period_days[i] for i in range(len(period_days)-1)]
        avg_gap = sum(gaps) / len(gaps)
        if 25 <= avg_gap <= 35:
            insights.append("Your cycles appear fairly regular.")
        else:
            insights.append("Your cycle length varies, which is common for many people.")

    # Mood pattern
    low_moods = sum(1 for m in mood_values if m <= 2 and m > 0)
    if low_moods > len(mood_values) * 0.4:
        insights.append("You’ve logged low moods often. Mood changes during cycles are common.")

    # Energy pattern
    low_energy = sum(1 for e in energy_values if e <= 2 and e > 0)
    if low_energy > len(energy_values) * 0.4:
        insights.append("You’ve been experiencing low energy frequently. Rest and nutrition matter 💗")

    # Most common symptom
    if symptom_counter:
        symptom, count = symptom_counter.most_common(1)[0]
        if count >= 3:
            insights.append(f"'{symptom}' is your most logged symptom.")

    if not insights:
        insights.append("Keep logging — more data will reveal clearer patterns 🌸")

    return insights
