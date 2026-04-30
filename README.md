# 🔥 BurnoutGuard – AI Productivity & Burnout Detection System

## 🚩 Problem Statement
Modern productivity tools track output but fail to detect **early burnout signals**.  
Burnout builds silently through behavioral drift (reduced efficiency, irregular work, stress imbalance).
Detect early burnout signals from productivity patterns.

## 💡 Solution
BurnoutGuard is an **AI-powered system** that:
- Learns individual productivity patterns
- Detects deviations from baseline behavior
- Predicts burnout risk using machine learning
- Provides actionable insights to improve performance
- AI-based system that tracks user activity and predicts burnout risk using ML.

---

## ⚙️ Features
- 📊 Burnout Score Prediction  
- 📈 Productivity Analytics Dashboard  
- 🧠 ML-based Pattern Detection  
- 📝 Daily Activity Tracking  
- 💡 Smart Recommendations ("What to improve tomorrow")  

---

## 🧠 Tech Stack
- **Frontend/UI**: Streamlit  
- **Backend**: Python  
- **Data Processing**: Pandas, NumPy  
- **Machine Learning**: Scikit-learn (RandomForest)  

---

## 🔍 How It Works
1. User inputs daily data (hours, tasks, stress, sleep, etc.)
2. System builds a personal baseline
3. ML model detects deviations
4. Burnout score is generated
5. Insights + recommendations are shown

---

## 🚀 Installation & Run
```bash
pip install -r requirements.txt
streamlit run app.py
