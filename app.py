import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
# UI improvements
git add .
git commit -m "Improved UI layout and structure"
    # Burnout logic added
    git add .
git commit -m "Added burnout score calculation logic"

git add .
git commit -m "Integrated ML model for prediction"

git add .
git commit -m "Added insights and recommendation system"

git add .
git commit -m "Final bug fixes and cleanup"

st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to", [
    "Input",
    "Dashboard",
    "Analytics",
    "Reports",
    "Settings"

])

st.set_page_config(page_title="AI Burnout Analyzer Pro", layout="wide")

st.title("🧠 AI Productivity Drift & Burnout Intelligence System")

# -------------------------
# LOAD DATA SAFELY
# -------------------------
columns = [
    "hours","tasks","mood","stress","sleep",
    "distraction","burnout_score","efficiency"
]

if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")

    for col in columns:
        if col not in df.columns:
            df[col] = 0

    df = df[columns]
else:
    df = pd.DataFrame(columns=columns)

df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

# -------------------------
# SIDEBAR INPUT
# -------------------------
st.sidebar.header("Daily Input")

hours = st.sidebar.number_input("Hours Worked", 1, 24, 1)
tasks = st.sidebar.number_input("Tasks Completed", 0, 50, 0)
mood = st.sidebar.slider("Mood (1=low,5=high)", 1, 5, 3)
stress = st.sidebar.slider("Stress (1=low,5=high)", 1, 5, 3)
sleep = st.sidebar.number_input("Sleep Hours", 0, 12, 6)
distraction = st.sidebar.selectbox("Distraction Level", ["Low","Medium","High"])

# -------------------------
# CORE COMPUTATION
# -------------------------
def compute_burnout_explained(mood, stress, sleep, distraction_val):
    parts = {
        "Mood Impact": (5 - mood) * 2,
        "Stress Impact": stress * 2,
        "Sleep Debt": (8 - sleep) * 1.5,
        "Distraction": distraction_val
    }
    total = sum(parts.values())
    return total, parts

# -------------------------
# SAVE DATA
# -------------------------
if st.sidebar.button("Analyze & Save"):

    distraction_val = {"Low":1,"Medium":2,"High":3}[distraction]

    burnout_score, breakdown = compute_burnout_explained(
        mood, stress, sleep, distraction_val
    )

    efficiency = tasks / hours if hours > 0 else 0

    new_row = pd.DataFrame([{
        "hours": hours,
        "tasks": tasks,
        "mood": mood,
        "stress": stress,
        "sleep": sleep,
        "distraction": distraction_val,
        "burnout_score": burnout_score,
        "efficiency": efficiency
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("data.csv", index=False)

    st.success("Data saved successfully!")

# -------------------------
# CLEAN DATA
# -------------------------
df = df.dropna()

# -------------------------
# DASHBOARD
# -------------------------
if len(df) > 0:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Burnout Trend")
        st.line_chart(df["burnout_score"])

    with col2:
        st.subheader("⚡ Efficiency Trend")
        st.line_chart(df["efficiency"])

    # -------------------------
    # BURNOUT SCORE EXPLANATION
    # -------------------------
    st.subheader("🧠 Burnout Score Explanation")

    if len(df) > 0:
        latest = df.iloc[-1]

        _, breakdown = compute_burnout_explained(
            latest["mood"],
            latest["stress"],
            latest["sleep"],
            latest["distraction"]
        )

        st.write("### Breakdown (Why score is high/low):")
        for k, v in breakdown.items():
            st.write(f"- {k}: {round(v,2)}")

        st.write(f"**Total Burnout Score:** {round(sum(breakdown.values()),2)}")

    # -------------------------
    # WEEKLY SUMMARY INSIGHTS
    # -------------------------
    st.subheader("📅 Weekly Summary Insights")

    last_7 = df.tail(7)

    if len(last_7) > 0:

        avg_eff = last_7["efficiency"].mean()
        avg_stress = last_7["stress"].mean()
        avg_sleep = last_7["sleep"].mean()

        st.write(f"📌 Avg Efficiency: {round(avg_eff,2)}")
        st.write(f"📌 Avg Stress: {round(avg_stress,2)}")
        st.write(f"📌 Avg Sleep: {round(avg_sleep,2)} hrs")

        if avg_eff < df["efficiency"].mean():
            st.warning("Efficiency declining this week")

        if avg_sleep < 6:
            st.warning("Sleep debt accumulating")

        if avg_stress > 3:
            st.warning("Stress levels elevated")

    # -------------------------
    # DRIFT DETECTION
    # -------------------------
    st.subheader("🚨 Productivity Drift")

    if len(df) >= 5:
        recent = df["efficiency"].tail(5).values

        if recent[-1] < np.mean(recent[:-1]):
            st.error("Productivity is dropping → Drift detected")
        else:
            st.success("Stable productivity pattern")

    # -------------------------
    # ML MODEL (RANDOM FOREST)
    # -------------------------
    st.subheader("🔮 AI Burnout Prediction (Random Forest)")

    if len(df) >= 5:

        X = df[["hours","tasks","stress","sleep","efficiency"]]
        y = df["burnout_score"]

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        model.fit(X, y)

        latest_input = X.iloc[-1].values.reshape(1, -1)
        predicted = model.predict(latest_input)[0]

        st.write(f"Predicted Burnout Score: **{round(predicted,2)}**")

        if predicted > 20:
            st.error("High burnout risk detected")
        elif predicted > 10:
            st.warning("Moderate risk emerging")
        else:
            st.success("Stable condition")

    # -------------------------
    # TOMORROW RECOMMENDER (IMPORTANT FEATURE)
    # -------------------------
    st.subheader("🎯 What should I change tomorrow?")

    if len(df) > 0:

        latest = df.iloc[-1]

        suggestions = []

        if latest["sleep"] < 6:
            suggestions.append("Increase sleep to 7–8 hours")

        if latest["stress"] > 3:
            suggestions.append("Reduce workload or add breaks")

        if latest["efficiency"] < df["efficiency"].mean():
            suggestions.append("Focus on deep work blocks (no distractions)")

        if latest["tasks"] / max(latest["hours"],1) < 2:
            suggestions.append("Improve task planning per hour")

        if len(suggestions) == 0:
            suggestions.append("Maintain current routine — stable performance")

        for s in suggestions:
            st.write("→ " + s)

    # -------------------------
    # DATA TABLE
    # -------------------------
    st.subheader("📋 Recent Data")
    st.dataframe(df.tail(10))

    if page == "Input":
    # your input form + submit code


    
         st.header("📊 Advanced Analytics")

         import numpy as np
         from sklearn.linear_model import LinearRegression

         if not os.path.exists("data.csv"):
           st.warning("No data available")
         else:
           df = pd.read_csv("data.csv")

           st.subheader("Dataset")
           st.write(df.tail())

        # -------------------------
        # 1. Correlation Analysis
        # -------------------------
           st.subheader("🔗 Correlation Analysis")

           corr = df.corr(numeric_only=True)
           st.write(corr)

        # -------------------------
        # 2. Burnout Prediction (ML)
        # -------------------------
           st.subheader("🤖 Burnout Prediction (Next Day)")

           if len(df) >= 5:

            X = df[["hours", "tasks", "sleep", "stress", "mood"]]
            y = df["burnout_score"]

            model = LinearRegression()
            model.fit(X, y)

            latest = X.iloc[-1].values.reshape(1, -1)
            prediction = model.predict(latest)[0]

            st.write(f"Predicted Burnout Score: {round(prediction,2)}")

            if prediction > 20:
                st.error("High burnout predicted")
            elif prediction > 10:
                st.warning("Moderate burnout predicted")
            else:
                st.success("Low burnout predicted")

           else:
            st.info("Need at least 5 records for prediction")

        # -------------------------
        # 3. Anomaly Detection
        # -------------------------
         st.subheader("🚨 Anomaly Detection")

         mean = df["burnout_score"].mean()
         std = df["burnout_score"].std()

         df["anomaly"] = abs(df["burnout_score"] - mean) > 2 * std

         anomalies = df[df["anomaly"] == True]

         if len(anomalies) > 0:
            st.warning("Anomalies detected")
            st.write(anomalies)
         else:
            st.success("No anomalies detected")

    elif page == "Reports":

        st.header("📄 Reports")

        if not os.path.exists("data.csv"):
          st.warning("No data available")
        else:
          df = pd.read_csv("data.csv")

        st.subheader("Full Report")
        st.write(df)

        # Summary
        st.subheader("Summary Statistics")
        st.write(df.describe())

        # Download CSV
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Report as CSV",
            data=csv,
            file_name="burnout_report.csv",
            mime="text/csv"
        )

    elif page == "Settings":

     st.header("⚙ Settings")

     st.subheader("Threshold Configuration")

     low_threshold = st.slider("Low Risk Threshold", 0, 20, 10)
     high_threshold = st.slider("High Risk Threshold", 10, 40, 20)

     st.write(f"Low Risk < {low_threshold}")
     st.write(f"High Risk > {high_threshold}")

     st.info("Note: This is a demo setting (not persisted)")

     st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)
     
     st.markdown(f"""
<div style='padding:15px; border-radius:10px; background-color:#eaf2ff'>
<h3>📌 Insight</h3>
<p>Your burnout trend is being actively monitored. Based on your recent data, the system is detecting behavioral patterns and risk levels.</p>
</div>
""", unsafe_allow_html=True)
