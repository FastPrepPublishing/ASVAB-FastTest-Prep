
import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASVAB Master Trainer", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("asvab_full_question_bank.csv")

df = load_data()

if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "mode" not in st.session_state:
    st.session_state.mode = None

def reset():
    st.session_state.current_q = 0
    st.session_state.answers = {}
    st.session_state.mode = None

st.title("🧠 ASVAB Master Trainer - by FastPrep Publishing")

if st.session_state.mode is None:
    st.subheader("Select Mode")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Practice Mode"):
            st.session_state.mode = "practice"
    with col2:
        if st.button("🎯 Exam Simulation"):
            st.session_state.mode = "exam"
    st.stop()

st.sidebar.button("🔄 Restart Test", on_click=reset)

questions = df.to_dict("records")
current = st.session_state.current_q
q = questions[current]

st.markdown(f"**Question {current + 1} of {len(questions)}**")
st.markdown(f"**Section**: {q['Section']}")
st.markdown(f"**{q['Question']}**")

options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
labels = ["A", "B", "C", "D"]

if current not in st.session_state.answers:
    user_answer = st.radio("Choose your answer:", options, index=None, key=f"q_{current}")
    if user_answer:
        index = options.index(user_answer)
        selected = labels[index]
        st.session_state.answers[current] = selected

        if selected == q["Correct Answer"]:
            st.success("Correct ✅")
        else:
            st.error(f"Incorrect ❌ Correct answer: {q['Correct Answer']}")
        st.info(f"Explanation: {q['Explanation']}")
else:
    st.info(f"You already answered: {st.session_state.answers[current]}")
    index = labels.index(q["Correct Answer"])
    st.markdown(f"✅ **Correct Answer: {q['Correct Answer']} - {options[index]}**")
    st.markdown(f"ℹ️ {q['Explanation']}")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Previous", disabled=(current == 0)):
        st.session_state.current_q -= 1
        st.rerun()
with col2:
    if st.button("➡️ Next", disabled=(current == len(questions) - 1)):
        st.session_state.current_q += 1
        st.rerun()

if current == len(questions) - 1 and len(st.session_state.answers) == len(questions):
    score = sum(1 for i, q in enumerate(questions) if st.session_state.answers.get(i) == q["Correct Answer"])
    st.success(f"🏁 Test Completed! Your Score: {score}/{len(questions)}")
    if st.button("🔁 Restart"):
        reset()
        st.rerun()
