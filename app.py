import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Strength Analyzer")
st.write("Upload your resume and get instant AI feedback")

# ---------- Job Role Selection ----------
role = st.selectbox(
    "Select Job Role",
    ["Data Scientist", "Python Developer", "AI Engineer", "Web Developer"]
)

# ---------- Skill Sets ----------
role_skills = {
    "Data Scientist": ["python", "machine learning", "statistics", "pandas", "numpy"],
    "Python Developer": ["python", "oop", "django", "flask", "api"],
    "AI Engineer": ["deep learning", "tensorflow", "pytorch", "computer vision"],
    "Web Developer": ["html", "css", "javascript", "react"]
}

# ---------- Upload Resume ----------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

if uploaded_file:
    text = extract_text(uploaded_file)

    skills = role_skills[role]
    found = [skill for skill in skills if skill in text]
    missing = list(set(skills) - set(found))

    score = int((len(found) / len(skills)) * 100)

    st.subheader("📊 Resume Analysis Result")

    st.metric("Resume Strength Score", f"{score}%")

    st.write("### ✅ Skills Found")
    st.success(", ".join(found) if found else "None")

    st.write("### ❌ Missing Skills")
    st.error(", ".join(missing) if missing else "None")

    # ---------- Feedback ----------
    if score >= 80:
        feedback = "Strong resume. Ready for interviews!"
    elif score >= 50:
        feedback = "Good resume, but improvement needed."
    else:
        feedback = "Weak resume. Consider adding more relevant skills."

    st.info(feedback)

    # ---------- Chart ----------
    fig, ax = plt.subplots()
    ax.bar(["Found", "Missing"], [len(found), len(missing)])
    st.pyplot(fig)
