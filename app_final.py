import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASVAB Exam Simulation", layout="wide")
st.title("🧠 ASVAB Master Trainer – Debug Mode")

try:
    df = pd.read_csv("asvab_exam_simulation.csv")
    st.success("✅ CSV loaded successfully.")
    st.write("First 5 rows:")
    st.write(df.head())
except Exception as e:
    st.error("❌ Error loading CSV file.")
    st.exception(e)

st.set_page_config(page_title="ASVAB Exam Simulation", layout="wide")
st.title("🧠 ASVAB Master Trainer – Full Exam Simulation")

# Carica il file CSV
df = pd.read_csv("asvab_exam_simulation.csv")

# Inizializza lo stato dell'app
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "done" not in st.session_state:
    st.session_state.done = False

# Mostra la domanda corrente
q = df.iloc[st.session_state.q_index]
st.subheader(f"{q['Section']} – Question {st.session_state.q_index + 1} / {len(df)}")
st.write(q["Question"])

# Mostra le opzioni
options = [q["Option A"], q["Option B"], q["Option C"], q["Option D"]]
selected = st.radio("Your answer:", options, key=st.session_state.q_index)

# Salva la risposta
for label, text in zip(["A", "B", "C", "D"], options):
    if selected == text:
        st.session_state.responses[st.session_state.q_index] = label

# Feedback se l'utente ha risposto
if st.session_state.q_index in st.session_state.responses:
    correct = q["Correct Answer"]
    user = st.session_state.responses[st.session_state.q_index]
    if user == correct:
        st.success(f"✅ Correct! Answer: {correct}")
    else:
        st.error(f"❌ Incorrect. Correct answer: {correct}")
    st.info(q["Explanation"])

# Navigazione
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.button("⬅️ Back") and st.session_state.q_index > 0:
        st.session_state.q_index -= 1
with col3:
    if st.button("Next ➡️") and st.session_state.q_index < len(df) - 1:
        st.session_state.q_index += 1

# Invio finale
if st.session_state.q_index == len(df) - 1 and st.button("✅ Submit Exam"):
    st.session_state.done = True

# Risultato finale
if st.session_state.done:
    total = len(st.session_state.responses)
    correct = sum(
        df.iloc[i]["Correct Answer"] == ans
        for i, ans in st.session_state.responses.items()
    )
    percent = round((correct / total) * 100)
    st.subheader("🏁 Exam Completed!")
    st.write(f"**✅ Correct answers:** {correct} / {total}")
    st.write(f"**📊 Score:** {percent}%")
    st.balloons()
