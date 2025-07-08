import pandas as pd
import streamlit as st

# Layout generale
st.set_page_config(page_title="ASVAB Exam Prep", layout="centered")
st.title("🧠 ASVAB Master Trainer – FastPrep")

# Menu modalità
mode = st.radio("📌 Choose Mode", ["Practice by Section", "Full Exam Simulation"])

# Caricamento file
df_practice = pd.read_csv("asvab_visual_practice_questions.csv")
df_sim = pd.read_csv("asvab_exam_simulation.csv")

# 👉 Modalità PRATICA
if mode == "Practice by Section":
    section = st.selectbox("📚 Choose a section", df_practice["Section"].unique())
    question = df_practice[df_practice["Section"] == section].sample(1).iloc[0]

    st.markdown(question["Formatted Question"])

    for opt in ["Option A", "Option B", "Option C", "Option D"]:
        st.button(question[opt])

    st.markdown("---")
    st.markdown(f"**✅ Correct Answer:** {question['Correct Answer']}")
    st.markdown(f"**🧠 Explanation:** {question['Explanation']}")

# 👉 Modalità SIMULAZIONE
elif mode == "Full Exam Simulation":
    st.info("📝 This mode simulates the real ASVAB P&P exam: 225 questions across all sections.")

    index = st.number_input("🔢 Question #", min_value=1, max_value=225, value=1)
    question = df_sim.iloc[index - 1]

    st.markdown(f"**🧪 Section: {question['Section']}**")
    st.markdown(f"**📖 Question:** {question['Question']}")

    for opt in ["Option A", "Option B", "Option C", "Option D"]:
        st.button(question[opt])

    st.markdown("---")
    st.markdown(f"**✅ Correct Answer:** {question['Correct Answer']}")
    st.markdown(f"**🧠 Explanation:** {question['Explanation']}")
