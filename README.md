# 🩺 AI & ML Based Lifestyle Disease Prediction System

🔗 Live Demo:
https://lifestyle-based-disease-prediction-gznbw9epuvrw4mtbm5yjy5.streamlit.app/

## 📌 Project Description

This project is an AI-powered healthcare application that predicts the risk of lifestyle-related diseases using Machine Learning models.

Diseases Predicted:
- Hypertension
- Diabetes
- Heart Disease

The system analyzes user lifestyle inputs such as sleep duration, stress level, heart rate, blood pressure, and daily steps. It predicts disease probability, estimates the possible timeframe of occurrence, explains contributing factors using Explainable AI (SHAP), and provides personalized preventive guidance.

## 🎯 Features

- Multi-disease risk prediction
- Probability estimation for each disease
- Risk timeframe estimation
- Explainable AI using SHAP (feature importance)
- Personalized disease-specific preventive guidance
- Interactive visualizations (pie charts)
- Deployed as a live web application using Streamlit

## 🛠 Technologies Used

- Frontend/UI: Streamlit
- Backend: Python
- Machine Learning: Scikit-learn
- Explainability: SHAP
- Data Processing: Pandas, NumPy
- Visualization: Matplotlib
- Model Storage: Joblib

## 📂 Project Structure

lifestyle-based-disease-prediction/

app.py
guidance.py
timeframe.py
report.py
train.py
requirements.txt
README.md

models/
hyper_model.pkl
dia_model.pkl
heart_model.pkl

## ⚙️ Installation

pip install -r requirements.txt

## ▶️ How to Run

1. Train the models (optional)
python train.py

2. Run the application
streamlit run app.py

## ⚙️ How It Works

1. User enters lifestyle data
2. ML models predict disease probabilities
3. SHAP explains top contributing factors
4. System estimates timeframe of risk
5. Personalized preventive guidance is generated

## 🎯 Use Cases

- Preventive healthcare systems
- Early disease risk detection
- Health monitoring applications
- AI + Healthcare academic projects

## 🧠 Key Highlights

- Combines Machine Learning with Explainable AI (SHAP)
- Provides personalized and disease-specific recommendations
- Deployed as a real-time interactive web application
- Modular and scalable project design

## 📈 Future Enhancements

- Integration with wearable devices
- Deep learning models
- OpenAI API integration
- User authentication
- Mobile app version

## 👨‍💻 Developed By

Gundukadi Abhishek
https://github.com/gundukadiabhishek-dev

⭐ If you like this project, consider giving it a star!
