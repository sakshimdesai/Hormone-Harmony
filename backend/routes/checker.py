from flask import request, render_template
from utils import login_required

@login_required
def symptom_checker():

    # SHOW FORM (GET request)
    if request.method == "GET":
        return render_template("symptom_checker.html")

    # PROCESS FORM (POST request)
    if request.method == "POST":
        age = int(request.form.get("age"))
        delay = int(request.form.get("delay"))
        pain = int(request.form.get("pain"))
        flow = request.form.get("flow")
        cycle = request.form.get("cycle_length")
        symptoms = request.form.getlist("symptoms")  # Get checked symptoms
        
        # Count PCOS-related symptoms
        pcos_symptom_count = len([s for s in symptoms if s != "none"])
        has_pcos_indicators = pcos_symptom_count >= 2
        
        # Initialize result variables
        result = ""
        color = ""
        message = ""
        recommendations = []
        concerns = []
        
        # ASSESSMENT LOGIC - Based on medical research about PCOS/PCOD
        
        # === SEVERE RED FLAGS (Immediate medical attention needed) ===
        if pain == 5 and flow == "very_heavy":
            result = "Seek medical care soon"
            color = "red"
            message = "Debilitating pain with very heavy flow can indicate conditions that need medical evaluation."
            concerns = [
                "Pain that prevents daily activities",
                "Very heavy bleeding (soaking through pads hourly)"
            ]
            recommendations = [
                "See a gynecologist within 1-2 weeks",
                "Track your symptoms daily until appointment",
                "Consider visiting ER if bleeding becomes uncontrollable"
            ]
        
        # === VERY HEAVY FLOW (potential anemia risk) ===
        elif flow == "very_heavy":
            result = "Consider seeing a doctor"
            color = "orange"
            message = "Very heavy bleeding that requires changing pads/tampons hourly or passing large clots may lead to anemia and should be evaluated."
            concerns = [
                "Soaking through protection hourly",
                "Large blood clots",
                "Risk of anemia (fatigue, dizziness)"
            ]
            recommendations = [
                "Schedule appointment with gynecologist",
                "Track flow intensity and duration",
                "Monitor for signs of anemia (extreme fatigue, pale skin)"
            ]
        
        # === PCOS PATTERN DETECTED ===
        elif (cycle in ["irregular_moderate", "irregular_severe"] or 
              (cycle == "regular_long" and delay > 7)) and has_pcos_indicators:
            result = "Consider PCOS screening"
            color = "orange"
            message = "Your pattern suggests possible PCOS. About 1 in 10 women have PCOS, and it's manageable with proper care."
            concerns = [
                f"Irregular cycles ({cycle.replace('_', ' ')})",
                f"Experiencing {pcos_symptom_count} PCOS-related symptoms",
                "Delayed period by {} days".format(delay) if delay > 0 else None
            ]
            concerns = [c for c in concerns if c]  # Remove None values
            recommendations = [
                "See a gynecologist for PCOS evaluation",
                "PCOS is diagnosed through symptoms, ultrasound, and blood tests",
                "Lifestyle changes (diet, exercise) can help manage PCOS",
                "PCOS is very common and treatable - you're not alone"
            ]
        
        # === IRREGULAR CYCLES (general) ===
        elif cycle in ["irregular_moderate", "irregular_severe"] or delay > 14:
            result = "Track this pattern"
            color = "yellow"
            message = "Irregular cycles are common, especially in teens and those approaching menopause. However, persistent irregularity can be worth discussing with a doctor."
            
            if age < 20:
                concerns = [
                    "Cycles can be irregular for first 2-3 years after starting periods",
                    "Hormones are still stabilizing at your age"
                ]
                recommendations = [
                    "Track your cycles for 3-6 months",
                    "If irregularity continues beyond 3 years from first period, see a doctor",
                    "Maintain healthy lifestyle (balanced diet, regular exercise)"
                ]
            elif age > 45:
                concerns = [
                    "Irregular cycles can be part of perimenopause",
                    "Hormonal changes are normal at this age"
                ]
                recommendations = [
                    "Track cycle changes",
                    "Discuss with doctor at next checkup",
                    "Learn about perimenopause symptoms"
                ]
            else:
                concerns = [
                    f"Period delayed by {delay} days" if delay > 0 else "Irregular cycle pattern",
                    "Persistent irregularity should be evaluated"
                ]
                recommendations = [
                    "Track cycles for 2-3 months using this app",
                    "If pattern continues, see a gynecologist",
                    "Consider PCOS screening if you have other symptoms"
                ]
        
        # === SEVERE PAIN (possible endometriosis or other conditions) ===
        elif pain >= 4:
            result = "Consider seeing a doctor"
            color = "orange"
            message = "Pain that significantly affects your daily activities or requires strong medication should be evaluated."
            concerns = [
                "Pain level {} (severe to debilitating)".format(pain),
                "Pain this severe isn't 'normal' even during periods"
            ]
            recommendations = [
                "See a gynecologist to rule out endometriosis or other conditions",
                "Track pain patterns (when it starts, what helps/doesn't help)",
                "Don't suffer in silence - severe period pain can be treated",
                "Try heat pads, gentle exercise, and over-the-counter pain relief"
            ]
        
        # === MODERATE CONCERNS ===
        elif (pain == 3 and flow == "heavy") or (delay >= 7 and cycle == "regular_normal"):
            result = "Monitor and track"
            color = "yellow"
            message = "This is somewhat outside the typical range but not necessarily concerning if it's a one-time occurrence."
            concerns = [
                "Moderate pain with heavy flow" if flow == "heavy" else None,
                f"Cycle delayed by {delay} days" if delay >= 7 else None
            ]
            concerns = [c for c in concerns if c]
            recommendations = [
                "Track this for the next 2-3 cycles",
                "If it becomes a pattern, consult a gynecologist",
                "Stress, diet changes, and illness can affect your cycle",
                "Practice self-care and stress management"
            ]
        
        # === NORMAL RANGE ===
        else:
            result = "This seems normal"
            color = "green"
            message = "Your cycle appears to be within typical ranges. Small variations are completely normal."
            concerns = []
            recommendations = [
                "Continue tracking your cycle to understand your personal pattern",
                "Every body is different - your 'normal' may differ from others",
                "Healthy lifestyle supports cycle regularity (sleep, nutrition, stress management)"
            ]
            
            if delay > 0:
                recommendations.append(f"A {delay}-day delay occasionally is normal, especially with stress or lifestyle changes")

        # === ADDITIONAL CONTEXT FOR ADOLESCENTS ===
        if age < 18 and result != "Seek medical care soon":
            message += " Note: Cycles often take 2-3 years to become regular after your first period."
        
        # === ADDITIONAL CONTEXT IF PCOS SYMPTOMS PRESENT (but not main concern) ===
        if pcos_symptom_count >= 1 and result not in ["Consider PCOS screening", "Seek medical care soon"]:
            recommendations.append(f"You noted {pcos_symptom_count} PCOS-related symptom(s) - mention these at your next doctor visit")

        return render_template(
            "checker_result.html",
            result=result,
            color=color,
            message=message,
            concerns=concerns,
            recommendations=recommendations,
            age=age,
            delay=delay,
            pain=pain,
            flow=flow,
            pcos_symptom_count=pcos_symptom_count
        )