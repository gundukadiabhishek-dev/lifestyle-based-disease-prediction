import streamlit as st
import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt

from timeframe import estimate_timeframe
from guidance import generate_guidance
from report import generate_pdf
st.set_page_config(
    page_title="AI Health Risk Analyzer",
    page_icon="🩺",
    layout="wide"
)

st.set_page_config(page_title="Lifestyle Disease Prediction", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#5f9cff,#b97fff);
    font-family: 'Segoe UI', sans-serif;
}

/* Title */
.title {
    font-size:38px;
    font-weight:bold;
    text-align:center;
    margin-bottom:10px;
    color:white;
}

/* Text visibility */
h1, h2, h3, h4, h5, h6, p, label, div {
    color: white !important;
}

/* Buttons */
.stButton > button {
    background-color: #1f2937;
    color: white;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    border: none;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #111827;
    transform: scale(1.05);
}

/* Download button */
.stDownloadButton > button {
    background-color: #16a34a;
    color: white;
    border-radius: 8px;
}

/* Fix alert visibility */
.stAlert {
    color: black !important;
    background-color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= STATE =================
if "page" not in st.session_state:
    st.session_state.page = "input"

# ======================================
# INPUT PAGE
# ======================================
if st.session_state.page == "input":

    st.markdown('<div class="title">Lifestyle Disease Prediction System</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", 10, 100, 30)
        sleep = st.number_input("Sleep Duration (hours)", 0.0, 12.0, 7.0)

    with col2:
        stress_label = st.selectbox("Stress Level", ["Low", "Moderate", "High"])
        stress_map = {"Low": 0, "Moderate": 1, "High": 2}
        stress = stress_map[stress_label]
        heart_rate = st.number_input("Heart Rate", 40, 200, 80)

    with col3:
        bp = st.number_input("Blood Pressure", 80, 200, 120)
        steps = st.number_input("Daily Steps", 0, 20000, 5000)

    st.markdown("---")

    if st.button("🔍 Predict Health Risk"):
        st.session_state.user_input = pd.DataFrame([{
            "Age": age,
            "Sleep Duration": sleep,
            "Stress Level": stress,
            "Heart Rate": heart_rate,
            "Blood Pressure": bp,
            "Daily Steps": steps
        }])

        st.session_state.page = "results"
        st.rerun()

# ======================================
# RESULT PAGE
# ======================================
elif st.session_state.page == "results":

    st.markdown('<div class="title">Prediction Results</div>', unsafe_allow_html=True)

    # Load models
    hyper_model = joblib.load("models/hyper_model.pkl")
    dia_model = joblib.load("models/dia_model.pkl")
    heart_model = joblib.load("models/heart_model.pkl")

    user_input = st.session_state.user_input

    # ================= PREDICTIONS =================
    h_prob = hyper_model.predict_proba(user_input)[0][1]
    d_prob = dia_model.predict_proba(user_input)[0][1]
    c_prob = heart_model.predict_proba(user_input)[0][1]

    overall_risk = (h_prob + d_prob + c_prob) / 3
    timeframe = estimate_timeframe(overall_risk)

    st.subheader("Overall Health Score")
    st.metric("Risk Score", f"{overall_risk*100:.2f}%")
    st.progress(int(overall_risk * 100))

    st.markdown("---")

    # ================= TIMEFRAME =================
    st.subheader("⏳ Risk Timeframe")
    st.write(f"**{timeframe}**")

    st.markdown("---")

    # ================= PIE CHARTS =================
    st.subheader("📊 Disease-wise Risk Breakdown")

    col1, col2, col3 = st.columns(3)

    colors = ["#e74c3c", "#2ecc71"]

    with col1:
        st.markdown("**Hypertension**")
        fig1, ax1 = plt.subplots()
        ax1.pie([h_prob, 1 - h_prob], labels=["Risk", "Safe"], autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        st.markdown("**Diabetes**")
        fig2, ax2 = plt.subplots()
        ax2.pie([d_prob, 1 - d_prob], labels=["Risk", "Safe"], autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    with col3:
        st.markdown("**Heart Disease**")
        fig3, ax3 = plt.subplots()
        ax3.pie([c_prob, 1 - c_prob], labels=["Risk", "Safe"], autopct='%1.1f%%', colors=colors, startangle=90)
        ax3.axis('equal')
        st.pyplot(fig3)

    st.markdown("---")

    # ================= SHAP =================
    def get_shap_explanation(model_pipeline, user_input):

        model = model_pipeline.named_steps["model"]
        scaler = model_pipeline.named_steps["scaler"]

        scaled_input = scaler.transform(user_input)

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(scaled_input)

        if isinstance(shap_values, list):
            values = shap_values[1][0]
        else:
            values = shap_values[0]

        values = np.array(values).flatten()
        features = list(user_input.columns)

        min_len = min(len(features), len(values))
        features = features[:min_len]
        values = values[:min_len]

        df = pd.DataFrame({
            "Feature": features,
            "Impact": values
        })

        df["Abs Impact"] = df["Impact"].abs()
        return df.sort_values(by="Abs Impact", ascending=False)

    st.subheader("🧠 Factors Affecting Your Health Risk")

    models = {
        "Hypertension": hyper_model,
        "Diabetes": dia_model,
        "Heart Disease": heart_model
    }

    for disease, model in models.items():
        st.write(f"### {disease}")

        impact_df = get_shap_explanation(model, user_input)

        for i in range(min(3, len(impact_df))):
            feature = impact_df.iloc[i]["Feature"]
            value = user_input[feature].values[0]

            if feature == "Blood Pressure":
                st.write(f"• Your blood pressure ({value}) is influencing your {disease.lower()} risk.")

            elif feature == "Daily Steps":
                st.write(f"• Your daily activity ({value} steps) is affecting your {disease.lower()} risk.")

            elif feature == "Sleep Duration":
                st.write(f"• Your sleep ({value} hours) is contributing to your {disease.lower()} risk.")

            elif feature == "Stress Level":
                st.write(f"• Your stress level is impacting your {disease.lower()} risk.")

            elif feature == "Heart Rate":
                st.write(f"• Your heart rate ({value}) is affecting your {disease.lower()} risk.")

            elif feature == "Age":
                st.write(f"• Your age ({value}) plays a role in your {disease.lower()} risk.")

        st.markdown("---")

    # ================= AI INSIGHT =================
    st.subheader("🧠 Overall AI Insight")

    if overall_risk > 0.7:
        st.write("Your health risk is high due to multiple lifestyle factors.")
    elif overall_risk > 0.4:
        st.write("Your risk is moderate. Some habits need improvement.")
    else:
        st.write("Your lifestyle is generally healthy.")

    st.markdown("---")

    # ================= GUIDANCE =================
    st.subheader("💡 Personalized Preventive Guidance")

    user_dict = {
        "Age": user_input["Age"].values[0],
        "Sleep Duration": user_input["Sleep Duration"].values[0],
        "Stress Level": user_input["Stress Level"].values[0],
        "Heart Rate": user_input["Heart Rate"].values[0],
        "Blood Pressure": user_input["Blood Pressure"].values[0],
        "Daily Steps": user_input["Daily Steps"].values[0],
    }

    advice = generate_guidance(user_dict, overall_risk)

    for line in advice:
        st.write("•", line)

    st.markdown("---")

    # ================= PDF =================
    st.subheader("📄 Download Health Report")

    disease_probs = {
        "Hypertension": h_prob,
        "Diabetes": d_prob,
        "Heart Disease": c_prob
    }

    if st.button("📄 Generate PDF Report"):

        file_path = generate_pdf(
            user_dict,
            overall_risk,
            timeframe,
            disease_probs,
            advice
        )

        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name="Health_Report.pdf",
                mime="application/pdf"
            )

    st.markdown("---")

    # ================= CONCLUSION =================
    st.subheader("Health Conclusion")

    if overall_risk > 0.7:
        st.error("🚨 High risk detected.")
    elif overall_risk > 0.4:
        st.warning("⚠️ Moderate risk.")
    else:
        st.success("✅ Low risk.")

    if st.button("⬅️ Back"):
        st.session_state.page = "input"
        st.rerun()