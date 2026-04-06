import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# ======================================
# LOAD DATASET
# ======================================

df = pd.read_csv("D:\\mini_project_3-2\\dataset\\lifestyle_perfect_dataset.csv")


# ======================================
# FEATURES (same as app.py)
# ======================================

features = [
    "Age",
    "Sleep Duration",
    "Stress Level",
    "Heart Rate",
    "Blood Pressure",
    "Daily Steps"
]

X = df[features]


# ======================================
# CREATE MODELS FOLDER
# ======================================

os.makedirs("models", exist_ok=True)


# ======================================
# RANDOM FOREST PIPELINE (ACCURACY)
# ======================================

def train_random_forest(target, name):

    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),   # important
        ("model", RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            random_state=42
        ))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("\n==============================")
    print(f"{name.upper()} - RANDOM FOREST")
    print("==============================")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    joblib.dump(pipeline, f"models/{name}.pkl")


# ======================================
# LOGISTIC REGRESSION PIPELINE (INTERPRETABLE)
# ======================================

def train_logistic(target, name):

    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("\n==============================")
    print(f"{name.upper()} - LOGISTIC REGRESSION")
    print("==============================")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    joblib.dump(pipeline, f"models/{name}_log.pkl")


# ======================================
# TRAIN ALL 3 DISEASE MODELS
# ======================================

diseases = [
    ("Hypertension", "hyper_model"),
    ("Diabetes", "dia_model"),
    ("Heart Disease", "heart_model")
]

for target, name in diseases:
    train_random_forest(target, name)
    train_logistic(target, name)


print("\n✅ ALL MODELS TRAINED SUCCESSFULLY!")