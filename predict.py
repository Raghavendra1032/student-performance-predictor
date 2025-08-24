import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="Student Performance Predictor", layout="wide")
st.title("🎓 Student Performance Predictor")

# -----------------------------
# Input Form
# -----------------------------
st.sidebar.header("Student Data Input")
attendance = st.sidebar.slider("Attendance (%)", 0, 100, 75)
past_score = st.sidebar.slider("Past Score (out of 100)", 0, 100, 70)
study_hours = st.sidebar.slider("Average Study Hours per Day", 0.0, 10.0, 3.0)

# -----------------------------
# Sample Dataset (for model training)
# -----------------------------
# Here we generate a dummy dataset for demo purposes
np.random.seed(42)
data = pd.DataFrame({
    "attendance": np.random.randint(50, 101, 50),
    "past_score": np.random.randint(50, 101, 50),
    "study_hours": np.random.uniform(0, 10, 50)
})
# Simulate the target score
data["score"] = (
    0.4 * data["attendance"] +
    0.4 * data["past_score"] +
    2 * data["study_hours"] +
    np.random.normal(0, 5, 50)
)

# -----------------------------
# Train Model
# -----------------------------
X = data[["attendance", "past_score", "study_hours"]]
y = data["score"]
model = LinearRegression()
model.fit(X, y)

# -----------------------------
# Prediction
# -----------------------------
input_df = pd.DataFrame({
    "attendance": [attendance],
    "past_score": [past_score],
    "study_hours": [study_hours]
})
predicted_score = model.predict(input_df)[0]

st.subheader("Predicted Score")
st.success(f"🎯 {predicted_score:.2f} / 100")

# -----------------------------
# Visualization
# -----------------------------
st.subheader("Visual Analysis")

# Scatter plot: past_score vs predicted
plt.figure(figsize=(8,5))
plt.scatter(data["past_score"], data["score"], label="Historical Data")
plt.scatter(past_score, predicted_score, color='red', label="Your Prediction", s=100)
plt.xlabel("Past Score")
plt.ylabel("Predicted Score")
plt.title("Past Scores vs Predicted Score")
plt.legend()
st.pyplot(plt)