import streamlit as st
import joblib
import numpy as np
from pathlib import Path

# -----------------------------
# Load saved model and vectorizer
# -----------------------------
@st.cache_resource
def load_model():
    # Get project root directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load TF-IDF vectorizer and trained model
    vectorizer = joblib.load(BASE_DIR / "model" / "tfidf_vectorizer.pkl")
    model = joblib.load(BASE_DIR / "model" / "logistic_regression_model.pkl")

    return vectorizer, model


# Load model and vectorizer
tfidf, model = load_model()

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="Kaiburr Complaint Text Classifier",
    layout="centered"
)

# -----------------------------
# App Title
# -----------------------------
st.title("💬 Kaiburr Complaint Text Classifier")
st.write(
    "Enter a consumer complaint below and the model will predict its category."
)

# -----------------------------
# User Input
# -----------------------------
user_input = st.text_area(
    "✍️ Paste complaint text here:",
    height=180
)

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Category"):

    if not user_input.strip():
        st.warning("Please enter a complaint first.")

    else:
        # Transform input using TF-IDF
        input_features = tfidf.transform([user_input])

        # Predict category
        prediction = model.predict(input_features)[0]

        # Category labels
        label_names = {
            0: "Credit Reporting",
            1: "Debt Collection",
            2: "Consumer Loan",
            3: "Mortgage"
        }

        st.success(f"🧠 Predicted Category: **{label_names[prediction]}**")
        st.info("Model: Logistic Regression (TF-IDF)\nAccuracy: 88.2%")
