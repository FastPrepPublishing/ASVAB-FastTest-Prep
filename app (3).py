
import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="ASVAB Exam Prep", layout="centered")

# Caricamento dati
@st.cache_data
def load_data():
    return pd.read_csv("asvab_exam_simulation.csv")

df = load_data()

# Modalità di utilizzo
mode = st.sidebar.radio("Select Mode:", ["Practice Mode", "Exam Simulation"])

# Stato iniziale
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.start_time = time.time()

def show_question(row):
    st.subheader(f"Section: {row['Section']}")
    st.write(f"**{row['Question']}**")

    options = [row["Option A"], row["Option B"], row["Option C"], row["Option D"]]
    selected = st.radio("Choose your answer:", options, index=None, key=f"q{st.session_state.current_q}")

    return selected, options

def show_results():
    st.success("✅ Exam Completed!")
    total = len(df)
    score = st.session_state.score
    st.metric("Your Score", f"{score} / {total}")
    st.progress(score / total)

    # Optional: show time taken
    elapsed = int(time.time() - st.session_state.start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    st.write(f"🕒 Time Taken: {minutes} minutes and {seconds} seconds")

# Modalità simulazione
if mode == "Exam Simulation":
    total_questions = len(df)
    question = df.iloc[st.session_state.current_q]

    st.title("📝 ASVAB Full Simulation")

    selected_answer, options = show_question(question)

    if selected_answer:
        correct_option = question[f"Option {question['Correct Answer']}"]
        if selected_answer == correct_option:
            st.session_state.score += 1
            st.success("Correct ✅")
        else:
            st.error(f"Incorrect ❌ The correct answer was: {correct_option}")
        st.session_state.answers[st.session_state.current_q] = selected_answer

        if st.session_state.current_q + 1 < total_questions:
            if st.button("Next ➡️"):
                st.session_state.current_q += 1
                st.experimental_rerun()
        else:
            show_results()

# Modalità pratica
else:
    st.title("📚 ASVAB Practice Mode")

    section = st.selectbox("Choose a section:", df["Section"].unique())
    section_df = df[df["Section"] == section].sample(frac=1).reset_index(drop=True)

    for i, row in section_df.iterrows():
        st.divider()
        st.write(f"**{i + 1}. {row['Question']}**")
        options = [row["Option A"], row["Option B"], row["Option C"], row["Option D"]]
        correct_option = row[f"Option {row['Correct Answer']}"]
        answer = st.radio("Select:", options, key=f"practice_{i}")
        if answer:
            if answer == correct_option:
                st.success("✅ Correct")
            else:
                st.error(f"❌ Incorrect. Correct answer: {correct_option}")
        st.caption(row["Explanation"])
