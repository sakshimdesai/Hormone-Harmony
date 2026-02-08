from flask import request, render_template, session
from datetime import datetime, timedelta
from utils import login_required
from db import get_db
import json

@login_required
def dashboard():
    """Display pattern visualization dashboard"""
    
    user_id = session.get('user_id')
    db = get_db()
    
    # Get time range filter (default: 30 days)
    days = request.args.get('days', '30')
    if days == 'all':
        cutoff_date = datetime(2000, 1, 1)  # Far past date to get all logs
    else:
        cutoff_date = datetime.now() - timedelta(days=int(days))
    
    # Fetch symptom logs
    logs = db.execute('''
        SELECT date, period_status, mood, energy, cravings, symptoms, notes
        FROM symptom_logs
        WHERE user_id = ? AND date >= ?
        ORDER BY date ASC
    ''', (user_id, cutoff_date.strftime('%Y-%m-%d'))).fetchall()
    
    # Initialize data structures
    dates = []
    period_status = []
    mood_values = []
    energy_values = []
    symptom_counter = {}
    
    # Process logs
    for log in logs:
        dates.append(log['date'])
        period_status.append(1 if log['period_status'] == 'yes' else 0)
        mood_values.append(log['mood'] if log['mood'] else 0)
        energy_values.append(log['energy'] if log['energy'] else 0)
        
        # Count symptoms
        if log['symptoms']:
            symptoms = log['symptoms'].split(',')
            for symptom in symptoms:
                symptom = symptom.strip()
                if symptom:
                    symptom_counter[symptom] = symptom_counter.get(symptom, 0) + 1
    
    # Get top 6 most common symptoms
    top_symptoms = sorted(symptom_counter.items(), key=lambda x: x[1], reverse=True)[:6]
    symptom_labels = [s[0] for s in top_symptoms]
    symptom_counts = [s[1] for s in top_symptoms]
    
    # Calculate summary statistics
    total_logs = len(logs)
    
    # Find last period date
    last_period_date = None
    days_since_period = None
    for log in reversed(logs):
        if log['period_status'] == 'yes':
            last_period_date = log['date']
            # Calculate days since
            log_date = datetime.strptime(log['date'], '%Y-%m-%d')
            days_since_period = (datetime.now() - log_date).days
            break
    
    # Calculate average mood
    if mood_values:
        valid_moods = [m for m in mood_values if m > 0]
        if valid_moods:
            avg_mood = sum(valid_moods) / len(valid_moods)
            mood_emojis = {1: '😢', 2: '😕', 3: '😐', 4: '🙂', 5: '😊'}
            avg_mood_emoji = mood_emojis.get(round(avg_mood), '😐')
        else:
            avg_mood_emoji = '😐'
    else:
        avg_mood_emoji = '😐'
    
    # Generate insights
    insights = generate_insights(logs, period_status, mood_values, energy_values, symptom_counter)
    
    # Prepare chart data
    chart_data = {
        'dates': dates,
        'period_status': period_status,
        'mood': mood_values,
        'energy': energy_values,
        'symptoms': {
            'labels': symptom_labels,
            'counts': symptom_counts
        }
    }
    
    return render_template(
        'dashboard.html',
        total_logs=total_logs,
        last_period_date=last_period_date,
        days_since_period=days_since_period,
        avg_mood_emoji=avg_mood_emoji,
        chart_data=chart_data,
        insights=insights
    )


def generate_insights(logs, period_status, mood_values, energy_values, symptom_counter):
    """Generate pattern insights from user data"""
    insights = []
    
    if len(logs) < 3:
        return ["Log for a few more days to see personalized insights!"]
    
    # Period regularity insight
    period_days = [i for i, status in enumerate(period_status) if status == 1]
    if len(period_days) >= 2:
        gaps = [period_days[i+1] - period_days[i] for i in range(len(period_days)-1)]
        if gaps:
            avg_gap = sum(gaps) / len(gaps)
            if avg_gap < 21:
                insights.append(f"Your cycles seem shorter than average (~{int(avg_gap)} days). This might be worth mentioning to your doctor.")
            elif avg_gap > 35:
                insights.append(f"Your cycles seem longer than average (~{int(avg_gap)} days). This is common with PCOS and worth discussing with a healthcare provider.")
            elif 25 <= avg_gap <= 35:
                insights.append(f"Your cycles appear fairly regular (~{int(avg_gap)} days).")
    
    # Mood patterns
    if mood_values and len(mood_values) >= 5:
        valid_moods = [m for m in mood_values if m > 0]
        if valid_moods:
            low_mood_count = sum(1 for m in valid_moods if m <= 2)
            if low_mood_count > len(valid_moods) * 0.4:
                insights.append("You've logged low moods frequently. Remember, mood changes are normal during your cycle, but if you're concerned, consider talking to someone.")
    
    # Energy patterns
    if energy_values and len(energy_values) >= 5:
        valid_energy = [e for e in energy_values if e > 0]
        if valid_energy:
            low_energy_count = sum(1 for e in valid_energy if e <= 2)
            if low_energy_count > len(valid_energy) * 0.5:
                insights.append("You've been experiencing low energy frequently. Make sure you're getting enough sleep, staying hydrated, and eating nutritious foods.")
    
    # Common symptoms
    if symptom_counter:
        most_common = max(symptom_counter.items(), key=lambda x: x[1])
        if most_common[1] >= 3:
            insights.append(f"'{most_common[0]}' is your most logged symptom ({most_common[1]} times). Track when this happens to identify triggers.")
    
    # Cravings pattern
    cravings_count = sum(1 for log in logs if log['cravings'] == 'yes')
    if cravings_count > len(logs) * 0.5:
        insights.append("You experience cravings frequently. This is normal! Try to have healthy snacks available and stay hydrated.")
    
    # Period-related symptoms
    if len(period_days) >= 1:
        # Check for symptoms around period days
        period_related_symptoms = []
        for day_idx in period_days:
            if day_idx < len(logs):
                log = logs[day_idx]
                if log['symptoms']:
                    period_related_symptoms.extend(log['symptoms'].split(','))
        
        if period_related_symptoms:
            from collections import Counter
            common_period_symptom = Counter(period_related_symptoms).most_common(1)
            if common_period_symptom:
                insights.append(f"You often experience '{common_period_symptom[0][0].strip()}' during your period.")
    
    if not insights:
        insights.append("Keep logging! More data will reveal clearer patterns.")
    
    return insights