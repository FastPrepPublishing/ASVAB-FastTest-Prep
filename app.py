# app.py – ASVAB Exam Prep by FastPrep Publishing
import pandas as pd
import streamlit as st

df = pd.read_csv("asvab_visual_practice_questions.csv")

st.set_page_config(page_title="ASVAB Exam Prep", layout="centered")
st.title("🧠 ASVAB Master Trainer – Practice Questions")

section = st.selectbox("📚 Choose a section", df["Section"].unique())

question = df[df["Section"] == section].sample(1).iloc[0]

st.markdown(question["Formatted Question"])
st.markdown(question["Visual Timer"])

for opt in ["Option A", "Option B", "Option C", "Option D"]:
    st.button(question[opt])

st.markdown("---")
st.markdown(f"**✅ Correct Answer:** {question['Correct Answer']}")
st.markdown(f"**🧠 Explanation:** {question['Explanation']}")
