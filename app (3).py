
import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="ASVAB Exam Prep", layout="centered")

# Load question bank
@st.cache_data
def load_data():
    df = pd.read_csv("asvab_full_practice_bank.csv")
    df.dropna(subset=["Question", "Correct Answer"], inplace=True)
    df = df[df["Correct Answer"].isin(["A", "B", "C", "D"])]
    return df

df = load_data()

# Initialize session state
if "mode" not in st.session_state:
    st.session_state.mode = "Practice"
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []

# Sidebar selection
st.sidebar.title("ASVAB FastPrep App")
mode = st.sidebar.radio("Choose Mode", ["Practice Mode", "Exam Simulation"])
st.session_state.mode = "Practice" if mode == "Practice Mode" else "Exam"

def reset_state():
    st.session_state.current_q = 0
    st.session_state.answers = {}
    st.session_state.start_time = time.time()
    if st.session_state.mode == "Exam":
        st.session_state.exam_questions = df.sample(n=225).reset_index(drop=True)
    else:
        st.session_state.exam_questions = df.sample(frac=1).reset_index(drop=True)

reset = st.sidebar.button("🔁 Restart Session", on_click=reset_state)

# Start session if not already
if not st.session_state.exam_questions:
    reset_state()

questions = st.session_state.exam_questions
total_q = len(questions)

# Timer display
if st.session_state.mode == "Exam":
    elapsed = int(time.time() - st.session_state.start_time)
    minutes_left = max(0, 154 - elapsed // 60)
    st.info(f"⏳ Time Remaining: {minutes_left} min")

# Display question
q = questions.iloc[st.session_state.current_q]
st.markdown(f"### Question {st.session_state.current_q + 1} of {total_q}")
st.markdown(f"**Section:** {q['Section']}")
st.markdown(f"**{q['Question']}**")

options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
user_answer = st.radio("Choose your answer:", options,
    index=-1,
    key=f"question_{st.session_state.current_q}"
)

# Submit button
if st.button("Submit Answer"):
    answer_letter = ["A", "B", "C", "D"][options.index(user_answer)]
    st.session_state.answers[st.session_state.current_q] = answer_letter

    if st.session_state.mode == "Practice":
        correct_letter = q["Correct Answer"]
        if answer_letter == correct_letter:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer: {correct_letter}")
        st.markdown(f"**Explanation:** {q['Explanation']}")
    else:
        # In Exam Mode, hide explanations and move forward
        pass

    # Advance question
    if st.session_state.current_q + 1 < total_q:
        st.session_state.current_q += 1
        st.experimental_rerun()
    else:
        st.success("🎉 Test Completed!")

        # Score report
        correct = sum(
            1 for i, ans in st.session_state.answers.items()
            if questions.iloc[i]["Correct Answer"] == ans
        )
        st.markdown(f"### ✅ Your Score: {correct} / {total_q}")
        percentage = round((correct / total_q) * 100, 2)
        st.markdown(f"**Percentage:** {percentage}%")

        if percentage >= 85:
            st.success("Excellent! You're ready for the ASVAB.")
        elif percentage >= 65:
            st.warning("Fair performance. More practice recommended.")
        else:
            st.error("Keep practicing to improve your score.")
