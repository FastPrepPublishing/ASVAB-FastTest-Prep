
import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="ASVAB Master Trainer", layout="wide")

@st.cache_data
def load_question_bank():
    return pd.read_csv("asvab_full_question_bank.csv")

@st.cache_data
def load_exam_simulation():
    return pd.read_csv("asvab_exam_simulation.csv")

# Session state defaults
if "mode" not in st.session_state:
    st.session_state.mode = None
if "exam_index" not in st.session_state:
    st.session_state.exam_index = 0
if "practice_index" not in st.session_state:
    st.session_state.practice_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "exam_started" not in st.session_state:
    st.session_state.exam_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

def show_menu():
    st.title("🧠 ASVAB Master Trainer – by FastTestPrep Publishing")
    st.subheader("Seleziona una modalità:")
    if st.button("📝 Practice Mode"):
        st.session_state.mode = "practice"
    if st.button("🧪 Exam Simulation"):
        st.session_state.mode = "exam"
        st.session_state.exam_started = True
        st.session_state.start_time = time.time()

def show_timer(start):
    elapsed = int(time.time() - start)
    remaining = max(0, 3600 - elapsed)
    mins, secs = divmod(remaining, 60)
    st.markdown(f"⏱ Tempo rimanente: **{mins:02}:{secs:02}**")

def practice_mode():
    st.title("📚 Practice Mode")
    df = load_question_bank()
    section = st.selectbox("Scegli una sezione", df["Section"].unique())
    section_df = df[df["Section"] == section].reset_index(drop=True)
    q = section_df.iloc[st.session_state.practice_index % len(section_df)]
    st.markdown(f"**{q['Question']}**")
    options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
    answer = st.radio("Scegli una risposta:", options, key=f"practice_q{st.session_state.practice_index}")
    if st.button("Conferma"):
        correct = q[f"Option {q['Correct Answer']}"]
        if answer == correct:
            st.success("✅ Corretto!")
        else:
            st.error(f"❌ Sbagliato! Risposta corretta: {correct}")
        st.info(f"📘 Spiegazione: {q['Explanation']}")
        st.session_state.practice_index += 1

def exam_mode():
    st.title("🧪 ASVAB Exam Simulation")
    show_timer(st.session_state.start_time)
    df = load_exam_simulation()

    if st.session_state.exam_index < len(df):
        q = df.iloc[st.session_state.exam_index]
        st.subheader(f"Domanda {st.session_state.exam_index + 1} di {len(df)}")
        st.markdown(f"**{q['Question']}**")
        options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
        selected_key = f"exam_q{st.session_state.exam_index}"
        user_answer = st.radio("Scegli una risposta:", options, key=selected_key)

        if st.button("Conferma risposta"):
            correct = q[f"Option {q['Correct Answer']}"]
            if user_answer == correct:
                st.session_state.score += 1
            st.session_state.answers.append((q['Question'], user_answer, correct))
            st.session_state.exam_index += 1
            st.experimental_rerun()
    else:
        st.success("🎉 Test completato!")
        st.metric("Punteggio finale", f"{st.session_state.score} / {len(df)}")
        if st.button("🔁 Ricomincia"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

# Pulsante di ritorno al menu principale
if st.button("🔙 Torna al menu principale"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Logica principale
if st.session_state.mode == "practice":
    practice_mode()
elif st.session_state.mode == "exam":
    exam_mode()
else:
    show_menu()
