def generate_guidance(data, risk):

    sleep = data["Sleep Duration"]
    stress = data["Stress Level"]
    bp = data["Blood Pressure"]
    hr = data["Heart Rate"]
    steps = data["Daily Steps"]
    age = data["Age"]

    advice = []
    issues = []

    # ================================
    # DETECT ISSUES
    # ================================
    if sleep < 6:
        issues.append("insufficient sleep")

    if stress == 2:
        issues.append("high stress")

    if steps < 5000:
        issues.append("low physical activity")

    if bp > 130:
        issues.append("high blood pressure")

    if hr > 100:
        issues.append("high heart rate")

    if age > 50:
        issues.append("age-related risk")

    # ================================
    # CONTEXT
    # ================================
    if issues:
        advice.append("Your current health profile indicates " + ", ".join(issues) + ".")

    # ================================
    # RISK MESSAGE
    # ================================
    if risk > 0.7:
        advice.append("Your risk is high. Immediate lifestyle improvements are required.")
    elif risk > 0.4:
        advice.append("Your risk is moderate. Improving habits can reduce risk.")
    else:
        advice.append("Your lifestyle is generally healthy. Maintain consistency.")

    # ===================================================
    # 🩺 HYPERTENSION
    # ===================================================
    if bp > 130:
        advice.extend([
            "Reduce salt intake (avoid processed foods, pickles, chips).",
            "Increase potassium intake (banana, coconut water, spinach).",
            "Consume foods rich in magnesium (nuts, seeds, whole grains).",
            "Practice daily relaxation techniques to reduce blood pressure.",
            "Drink adequate water (2.5–3 liters daily).",
            "Avoid excessive caffeine and alcohol.",
            "Include garlic and beetroot in your diet.",
            "Engage in at least 30 minutes of physical activity daily.",
            "Monitor blood pressure regularly.",
            "Follow DASH diet (Dietary Approaches to Stop Hypertension).",

            # EXTRA
            "Avoid packaged foods high in sodium.",
            "Practice deep breathing exercises regularly.",
            "Maintain a healthy weight.",
            "Limit red meat consumption.",
            "Consume low-fat dairy products.",
            "Maintain work-life balance to reduce stress."
        ])

    # ===================================================
    # 🍬 DIABETES
    # ===================================================
    if steps < 5000 or age > 45:
        advice.extend([
            "Reduce sugar intake (avoid sweets and sugary drinks).",
            "Eat fiber-rich foods (oats, vegetables, legumes).",
            "Include whole grains instead of refined carbohydrates.",
            "Consume Vitamin C rich foods (lemon, oranges, amla).",
            "Maintain regular meal timings.",
            "Drink enough water to regulate blood sugar.",
            "Exercise regularly to improve insulin sensitivity.",
            "Avoid late-night eating habits.",
            "Monitor blood glucose levels.",
            "Include cinnamon and fenugreek in your diet.",

            # EXTRA
            "Avoid white bread and refined carbs.",
            "Include protein-rich foods (eggs, pulses).",
            "Eat smaller frequent meals.",
            "Include bitter gourd (karela) in diet.",
            "Stay hydrated throughout the day.",
            "Take short walks after meals."
        ])

    # ===================================================
    # ❤️ HEART DISEASE
    # ===================================================
    if hr > 100 or bp > 130:
        advice.extend([
            "Reduce intake of fried and junk food.",
            "Include healthy fats (nuts, seeds, olive oil).",
            "Eat omega-3 rich foods (fish, flaxseeds, walnuts).",
            "Increase fruits and green vegetables.",
            "Avoid smoking and alcohol.",
            "Maintain a healthy weight.",
            "Engage in cardiovascular exercises.",
            "Reduce stress levels.",
            "Ensure at least 7 hours of sleep.",
            "Get regular health check-ups.",

            # EXTRA
            "Avoid trans fats in processed foods.",
            "Consume antioxidant-rich foods.",
            "Practice breathing exercises.",
            "Limit salt intake.",
            "Maintain a consistent sleep routine.",
            "Reduce sedentary behavior."
        ])

    # ===================================================
    # 🧠 COMBINED CONDITIONS
    # ===================================================
    if sleep < 6 and stress == 2:
        advice.append("Poor sleep and high stress together significantly increase health risks.")

    if steps < 5000 and bp > 130:
        advice.append("Low activity and high blood pressure together increase cardiovascular risk.")

    if stress == 2 and hr > 100:
        advice.append("High stress and elevated heart rate can strain your heart.")

    # ===================================================
    # 🌿 UNIVERSAL NUTRITION
    # ===================================================
    advice.extend([
        "Ensure adequate Vitamin C intake (lemon, oranges, amla).",
        "Include iron-rich foods (spinach, lentils).",
        "Consume calcium-rich foods (milk, curd).",
        "Add fiber-rich foods to improve digestion.",
        "Drink sufficient water daily.",
        "Avoid excessive processed food."
    ])

    # ===================================================
    # FALLBACK
    # ===================================================
    if not issues:
        advice.append("No major issues detected. Continue maintaining your healthy lifestyle.")

    # LIMIT OUTPUT (IMPORTANT)
    advice = advice[:18]

    return advice