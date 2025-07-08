# app.py – ASVAB Exam Prep by FastPrep Publishing (Corretto)
import pandas as pd
import streamlit as st

# Impostazioni layout
st.set_page_config(page_title="ASVAB Exam Simulation", layout="wide")
st.title("🧠 ASVAB Master Trainer – Full Simulation Mode")

# Caricamento file della simulazione
df_sim = pd.read_csv("asvab_exam_simulation.csv")

# Inizializzazione session state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Funzione per calcolo punteggio finale
def calculate_score():
    correct = 0
    for i, ans in st.session_state.answers.items():
        if df_sim.iloc[i]["Correct Answer"] == ans:
            correct += 1
    total = len(st.session_state.answers)
    return correct, total, round((correct / total) * 100)

# Navigazione tra domande
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️ Back") and st.session_state.current_q > 0:
        st.session_state.current_q -= 1
with col3:
    if st.button("Next ➡️") and st.session_state.current_q < len(df_sim) - 1:
        st.session_state.current_q += 1

# Estrai la domanda attuale
q = df_sim.iloc[st.session_state.current_q]

# Visualizza domanda
st.markdown(f"**🧪 Section: {q['Section']}**")
st.markdown(f"**📖 Question {st.session_state.current_q + 1} of {len(df_sim)}:** {q['Question']}")

# Opzioni di risposta senza preselezione
options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
selected = st.radio("Choose your answer:", options, index=None, key=f"question_{st.session_state.current_q}")

# Salvataggio risposta selezionata
if selected:
    for label, text in zip(["A", "B", "C", "D"], options):
        if selected == text:
            st.session_state.answers[st.session_state.current_q] = label

# Mostra feedback solo dopo risposta
if st.session_state.current_q in st.session_state.answers:
    correct = q["Correct Answer"]
    if st.session_state.answers[st.session_state.current_q] == correct:
        st.success(f"✅ Correct! The answer is {correct}")
    else:
        st.error(f"❌ Incorrect. The correct answer is {correct}")
    st.info(f"🧠 Explanation: {q['Explanation']}")

# Simulazione timer per sezione (visuale)
timer_bar = "⏱️ Time Remaining: " + "🟩" * 7 + "⬜" * 3
st.markdown(timer_bar)

# Invio finale
if st.session_state.current_q == len(df_sim) - 1:
    if st.button("✅ Submit Test"):
        st.session_state.submitted = True

# Risultato finale
if st.session_state.submitted:
    correct, total, percent = calculate_score()
    st.markdown("## 🏁 Test Completed!")
    st.markdown(f"**✅ Correct Answers:** {correct} / {total}")
    st.markdown(f"**📊 Score:** {percent}%")
    if percent >= 60:
        st.success("🎉 Good job! You are likely to pass the ASVAB.")
    else:
        st.warning("⚠️ Keep practicing! Aim for 60% or more.")
    st.balloons()
