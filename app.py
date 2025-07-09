
import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="ASVAB FastPrep", layout="wide")
st.title("📘 ASVAB Exam Prep - FastPrep Publishing")

@st.cache_data
def load_questions():
    df = pd.read_csv("asvab_exam_simulation.csv")
    return df

df = load_questions()

mode = st.sidebar.radio("Choose Mode", ["Practice", "Full Exam Simulation"])

if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if mode == "Practice":
    st.subheader("🧠 Practice Mode")
    question = df.sample(1).iloc[0]
    st.markdown(f"**Section:** {question['Section']}")
    st.markdown(f"**Question:** {question['Question']}")

    options = [
        question["Option A"],
        question["Option B"],
        question["Option C"],
        question["Option D"],
    ]
    default_option = "Select an answer"
    user_answer = st.selectbox("Choose your answer:", [default_option] + options)

    if user_answer != default_option:
        if user_answer == question[f"Option {question['Correct Answer']}"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer: Option {question['Correct Answer']}")
        st.info(f"Explanation: {question['Explanation']}")

else:
    st.subheader("📝 Full Exam Simulation Mode")
    total_questions = 15
    duration_minutes = 10
    duration_seconds = duration_minutes * 60

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = duration_seconds - elapsed
    if remaining <= 0:
        st.warning("⏰ Time's up!")
        show_results = True
    else:
        mins, secs = divmod(remaining, 60)
        st.info(f"Time Remaining: {mins:02d}:{secs:02d}")
        show_results = False

    if "exam_set" not in st.session_state:
        st.session_state.exam_set = df.sample(total_questions).reset_index(drop=True)

    if st.session_state.current_q < total_questions and not show_results:
        q = st.session_state.exam_set.iloc[st.session_state.current_q]
        st.markdown(f"**Question {st.session_state.current_q + 1}/{total_questions}**")
        st.markdown(f"**Section:** {q['Section']}")
        st.markdown(f"**Question:** {q['Question']}")

        options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
        default_option = "Select an answer"
        user_answer = st.selectbox(
            "Choose your answer:",
            [default_option] + options,
            key=f"question_{st.session_state.current_q}"
        )

        if user_answer != default_option:
            correct_option = q[f"Option {q['Correct Answer']}"]
            if user_answer == correct_option:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct answer: {correct_option}")
            st.info(f"Explanation: {q['Explanation']}")
            st.session_state.answers[st.session_state.current_q] = user_answer
            if st.button("Next"):
                st.session_state.current_q += 1
                st.rerun()
    else:
        score = 0
        for i, q in st.session_state.exam_set.iterrows():
            user_ans = st.session_state.answers.get(i, "")
            correct_ans = q[f"Option {q['Correct Answer']}"]
            if user_ans == correct_ans:
                score += 1
        st.success(f"🎉 Test completed! Your Score: {score}/{total_questions}")
        st.balloons()
        if st.button("Restart Test"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
