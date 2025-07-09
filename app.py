import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="ASVAB Exam Prep", layout="centered")

@st.cache_data
def load_data():
    return pd.read_csv("asvab_exam_simulation.csv")

df = load_data()

def run_exam_simulation():
    st.title("📝 ASVAB Full Exam Simulation")

    num_questions = 3
    exam_time = 3 * 60

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
        st.session_state.exam_index = 0
        st.session_state.score = 0
        st.session_state.answers = {}

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, exam_time - elapsed)
    mins, secs = divmod(remaining, 60)
    st.warning(f"⏱️ Time Remaining: {mins:02d}:{secs:02d}")

    if remaining == 0:
        st.session_state.exam_index = num_questions

    if st.session_state.exam_index < num_questions:
        q = df.iloc[st.session_state.exam_index]
        st.markdown(f"**Question {st.session_state.exam_index + 1}:** {q['Question']}")
        options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
        user_choice = st.radio("Choose your answer:", options, index=None, key=f"q{st.session_state.exam_index}")

        if st.button("Submit", key=f"submit_{st.session_state.exam_index}"):
            correct_option = q[f"Option {q['Correct Answer']}"]
            st.session_state.answers[st.session_state.exam_index] = user_choice

            if user_choice == correct_option:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: {correct_option}")

            st.session_state.exam_index += 1
            st.experimental_rerun()
    else:
        st.success(f"✅ Exam Finished! Your score: {st.session_state.score}/{num_questions}")

def run_practice_mode():
    st.title("🎯 Practice Mode")
    section = st.selectbox("Choose section:", sorted(df["Section"].unique()))
    filtered = df[df["Section"] == section].sample(frac=1).reset_index(drop=True)

    for i, row in filtered.iterrows():
        st.markdown(f"**{i + 1}. {row['Question']}**")
        options = [row["Option A"], row["Option B"], row["Option C"], row["Option D"]]
        choice = st.radio("Your answer:", options, index=None, key=f"practice_{i}")
        if choice:
            correct = row[f"Option {row['Correct Answer']}"]
            if choice == correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct answer: {correct}")
            st.info(f"ℹ️ Explanation: {row['Explanation']}")

mode = st.sidebar.selectbox("Choose Mode", ["Practice Mode", "Exam Simulation"])

if mode == "Practice Mode":
    run_practice_mode()
else:
    run_exam_simulation()
