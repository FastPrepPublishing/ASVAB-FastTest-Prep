
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="ASVAB Master Trainer", layout="centered")

# Caricamento dati
@st.cache_data
def load_data():
    return pd.read_csv("asvab_sample_questions.csv")

df = load_data()

if "mode" not in st.session_state:
    st.session_state.mode = None

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

st.title("📚 ASVAB Master Trainer - by FastPrep Publishing")

# Modalità
if st.session_state.mode is None:
    st.subheader("Scegli la modalità:")
    if st.button("✅ Practice Mode"):
        st.session_state.mode = "practice"
        st.rerun()
    elif st.button("🎯 Exam Simulation"):
        st.session_state.mode = "exam"
        df = df.sample(frac=1).reset_index(drop=True)
        st.rerun()

# Funzione per mostrare domanda
def show_question():
    q = df.iloc[st.session_state.current_q]
    st.markdown(f"**Sezione:** {q['Section']}")
    st.markdown(f"**Domanda {st.session_state.current_q + 1} / {len(df)}:** {q['Question']}")
    options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
    answer = st.radio("Scegli la risposta:", options, index=None, key=f"q_{st.session_state.current_q}")
    if st.button("Invia"):
        if answer:
            correct = q[f"Option {q['Correct Answer']}"]
            is_correct = answer == correct
            st.session_state.answers[st.session_state.current_q] = (answer, is_correct)
            if is_correct:
                st.success("✅ Corretto!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Errato. Risposta corretta: {correct}")
                st.info(f"ℹ️ Spiegazione: {q['Explanation']}")
            if st.session_state.current_q + 1 < len(df):
                st.button("Prossima domanda", on_click=lambda: st.session_state.update({"current_q": st.session_state.current_q + 1}), key=f"next_{st.session_state.current_q}")
            else:
                st.button("Mostra risultati finali", on_click=lambda: st.session_state.update({"current_q": len(df)}))

# Visualizzazione domande o risultati
if st.session_state.current_q < len(df):
    show_question()
else:
    st.subheader("📊 Risultati finali")
    st.write(f"Punteggio finale: {st.session_state.score} su {len(df)}")
    percent = int((st.session_state.score / len(df)) * 100)
    st.progress(percent)
    st.balloons()
    if st.button("🔁 Ricomincia"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
